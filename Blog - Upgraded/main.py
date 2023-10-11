import flask
from typing import List
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField, CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import EmailField, StringField, PasswordField, validators, URLField, SubmitField
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from functools import wraps
from datetime import datetime
from flask_gravatar import Gravatar
import smtplib
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///posts.db')
app.secret_key = os.environ.get('secretkey')
ckeditor = CKEditor(app)

login_manager = LoginManager()

gravatar = Gravatar(app,
                    size=40,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)
bootstrap = Bootstrap5(app)
login_manager.init_app(app)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = 'user_table'

    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    # Children links
    posts: Mapped[List['BlogPost']] = relationship(back_populates='author')
    comments: Mapped[List['Comment']] = relationship(back_populates='author')


class BlogPost(db.Model):
    __tablename__ = 'blogpost_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)

    # Parent links
    author: Mapped['User'] = relationship(back_populates='posts')
    author_id: Mapped[int] = mapped_column(ForeignKey('user_table.id', ondelete='CASCADE'), nullable=False)

    # Children links
    comments: Mapped[List['Comment']] = relationship(back_populates='post')


class Comment(db.Model):
    __tablename__ = 'comment_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    body: Mapped[str] = mapped_column(String, nullable=False)

    # Parents' links
    post: Mapped['BlogPost'] = relationship(back_populates='comments')
    post_id: Mapped[int] = mapped_column(ForeignKey('blogpost_table.id', ondelete='CASCADE'), nullable=False)

    author: Mapped[User] = relationship(back_populates='comments')
    author_id: Mapped[int] = mapped_column(ForeignKey('user_table.id', ondelete='CASCADE'), nullable=False)


with app.app_context():
    db.create_all()
    all_blog_posts = BlogPost.query.all()


# Form
class NewPostForm(FlaskForm):
    title = StringField('Blog Post Title', validators=[validators.input_required()])
    subtitle = StringField('Subtitle', validators=[validators.input_required()])
    img_url = URLField('Blog Image URL', validators=[validators.input_required()])
    body = CKEditorField('Blog Content', validators=[validators.input_required()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[validators.input_required()])
    name = StringField('Name', validators=[validators.input_required()])
    password = PasswordField('Password', validators=[validators.input_required()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[validators.input_required()])
    password = PasswordField('Password', validators=[validators.input_required()])
    submit = SubmitField('Login')


class CommentForm(FlaskForm):
    body = CKEditorField('Comment', validators=[validators.input_required()])
    submit = SubmitField('Submit Comment')


# Email section
username = os.getenv('email')
password = os.getenv('password')


def send_email(message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=username, password=password)
        connection.sendmail(
            from_addr=username,
            to_addrs=username,
            msg=f'Subject:New message\n\n {message}'
        )


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.id != 1:
            return flask.abort(code=403)
        return func(*args, **kwargs)
    return decorated_view


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route('/')
@app.route('/index')
def show_main():
    global all_blog_posts
    all_blog_posts = BlogPost.query.all()
    return render_template(
        'index.html',
        data_json=all_blog_posts,
        current_user=current_user
    )


@app.route('/about')
def show_about():
    return render_template('about.html', logged_in=current_user.is_authenticated)


@app.route('/contact', methods=['POST', 'GET'])
def show_contact():
    if request.method == 'GET':
        return render_template('contact.html', logged_in=current_user.is_authenticated)
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        message = request.form.get('message')
        send_email(f'Name: {name}\nEmail: {email}\nPhone number: {phone_number}\n Message: {message}')
        return redirect(url_for('show_contact', _method='GET'))


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    ids = [blog.id for blog in all_blog_posts]
    index = ids.index(post_id)
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                author_id=current_user.id,
                post_id=post_id,
                body=comment_form.body.data
            ) 

            db.session.add(new_comment)
            db.session.commit()
        else:
            flash('You need to login')
            return redirect(url_for('login'))

    comments = db.session.scalars(db.select(Comment).filter_by(post_id=post_id))

    return render_template('post.html',
                           data_json=all_blog_posts[index],
                           current_user=current_user,
                           comment_form=comment_form,
                           comments=comments
                           )


@app.route('/new-post', methods=['GET', 'POST'])
@admin_required
def new_post():
    new_form = NewPostForm()
    if new_form.validate_on_submit():
        title = new_form.title.data
        subtitle = new_form.subtitle.data
        img_url = new_form.img_url.data
        body = new_form.body.data
        date_today = datetime.now().today().date().strftime("%B %d, %Y")

        new_blog_post = BlogPost(
            title=title,
            subtitle=subtitle,
            img_url=img_url,
            body=body,
            date=date_today,
            author_id=current_user.id
        )
        db.session.add(new_blog_post)
        db.session.commit()
        return redirect(url_for('show_main'))
    return render_template('make-post.html', form=new_form)


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@admin_required
def edit_post(post_id):
    found_blog_post = db.get_or_404(BlogPost, post_id)
    new_form = NewPostForm()
    if request.method == 'GET':
        new_form.title.data = found_blog_post.title
        new_form.subtitle.data = found_blog_post.subtitle
        new_form.img_url.data = found_blog_post.img_url
        new_form.body.data = found_blog_post.body
        new_form.date = found_blog_post.date

    if new_form.validate_on_submit():
        found_blog_post.title = new_form.title.data
        found_blog_post.subtitle = new_form.subtitle.data
        found_blog_post.img_url = new_form.img_url.data
        found_blog_post.body = new_form.body.data
        db.session.commit()
        return redirect(url_for('show_main'))
    return render_template('make-post.html', form=new_form, data=found_blog_post)


@app.route('/delete/<int:post_id>')
@admin_required
def delete_post(post_id):
    found_post = db.get_or_404(BlogPost, post_id)
    db.session.delete(found_post)
    db.session.commit()
    return redirect(url_for('show_main'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        new_user = User()
        new_user.email = register_form.email.data
        new_user.name = register_form.name.data
        new_user.password = generate_password_hash(password=register_form.password.data, salt_length=8)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('show_main'))

    return render_template('register.html', form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        found_user = db.session.scalar(db.select(User).filter_by(email=form.email.data))
        if not found_user or not check_password_hash(found_user.password, form.password.data):
            return redirect(url_for('login'))
        login_user(found_user)
        return redirect(url_for('show_main'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('show_main'))


if __name__ == '__main__':
    app.run()
