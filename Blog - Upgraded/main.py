from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField, CKEditor
from wtforms import StringField, validators, URLField, SubmitField
from datetime import datetime
import smtplib
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.secret_key = 'isSecretKey'
ckeditor = CKEditor(app)

bootstrap = Bootstrap5(app)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()
    all_blog_posts = BlogPost.query.all()


# Form
class NewPostForm(FlaskForm):
    title = StringField('Blog Post Title', validators=[validators.input_required()])
    subtitle = StringField('Subtitle', validators=[validators.input_required()])
    author = StringField('Name of the Author', validators=[validators.input_required()])
    img_url = URLField('Blog Image URL', validators=[validators.input_required()])
    body = CKEditorField('Blog Content', validators=[validators.input_required()])
    submit = SubmitField('Submit')


# Email section
username = os.getenv('email')
password = os.getenv('password')


def send_email(message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=username, password=password)
        connection.sendmail(
            from_addr=username,
            to_addrs='username@email.com',
            msg=f'Subject:New message\n\n {message}'
        )


@app.route('/')
@app.route('/index')
def show_main():
    global all_blog_posts
    all_blog_posts = BlogPost.query.all()
    return render_template('index.html', data_json=all_blog_posts)


@app.route('/about')
def show_about():
    return render_template('about.html')


@app.route('/contact', methods=['POST', 'GET'])
def show_contact():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        message = request.form.get('message')
        send_email(f'Name: {name}\nEmail: {email}\nPhone number: {phone_number}\n Message: {message}')
        return redirect(url_for('show_contact', _method='GET'))


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return render_template('post.html', data_json=all_blog_posts[post_id-1])


@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    new_form = NewPostForm()
    if new_form.validate_on_submit():
        title = new_form.title.data
        subtitle = new_form.subtitle.data
        author = new_form.author.data
        img_url = new_form.img_url.data
        body = new_form.body.data
        date_today = datetime.now().today().date().strftime("%B %d, %Y")

        new_blog_post = BlogPost(
            title=title,
            subtitle=subtitle,
            author=author,
            img_url=img_url,
            body=body,
            date=date_today
        )
        db.session.add(new_blog_post)
        db.session.commit()
        return redirect(url_for('show_main'))
    return render_template('make-post.html', form=new_form)


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    found_blog_post = db.get_or_404(BlogPost, post_id)
    new_form = NewPostForm()
    if request.method == 'GET':
        new_form.title.data = found_blog_post.title
        new_form.subtitle.data = found_blog_post.subtitle
        new_form.author.data = found_blog_post.author
        new_form.img_url.data = found_blog_post.img_url
        new_form.body.data = found_blog_post.body
        new_form.date = found_blog_post.date

    if new_form.validate_on_submit():
        found_blog_post.title = new_form.title.data
        found_blog_post.subtitle = new_form.subtitle.data
        found_blog_post.author = new_form.author.data
        found_blog_post.img_url = new_form.img_url.data
        found_blog_post.body = new_form.body.data
        db.session.commit()
        return redirect(url_for('show_main'))
    return render_template('make-post.html', form=new_form, data=found_blog_post)


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    found_post = db.get_or_404(BlogPost, post_id)
    db.session.delete(found_post)
    db.session.commit()
    return redirect(url_for('show_main'))


if __name__ == '__main__':
    app.run(debug=True)
