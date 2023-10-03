import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests

MOVIE_API_ENDPOINT = 'https://api.themoviedb.org/3/search/movie'
MOVIE_API_DETAILED_ENDPOINT = 'https://api.themoviedb.org/3/movie/'
MOVIE_POSTER_PATH_PREFIX = 'https://image.tmdb.org/t/p/w500'
ACCESS_TOKEN = os.environ.get('access_token_movie')

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
Bootstrap5(app)


db.init_app(app)


class EditForm(FlaskForm):
    rating = FloatField('Your rating out of 10 e.g 7.5', validators=[DataRequired()])
    review = StringField('Your review', validators=[DataRequired()])
    submit = SubmitField()


class AddForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


def add_movie(title: str, year: int, description: str, img_url: str):
    try:
        max_id = db.session.query(db.func.max(Movie.id)).scalar()

        new_movie = Movie()
        new_movie.id = max_id + 1
        new_movie.title = title
        new_movie.year = year
        new_movie.description = description
        new_movie.img_url = img_url
        new_movie.rating = 0
        new_movie.ranking = 0
        new_movie.review = "No Review Yet"

        db.session.add(new_movie)
        db.session.commit()
        return new_movie
    except Exception as e:
        print(e)
        db.session.rollback()
        db.session.flush()
        return None


def update_movie(movie_id: int, movie_rating, movie_review):
    try:
        book = db.get_or_404(Movie, movie_id)
        book.rating = movie_rating
        book.review = movie_review
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return False


def delete_movie(movie_id: int):
    global db
    try:
        book = db.get_or_404(Movie, movie_id)
        db.session.delete(book)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(e)
        return False


@app.route("/")
def home():
    # movies = Movie.query.all()
    movies = db.session.scalars(db.select(Movie).order_by(Movie.rating)).all()

    for movie in movies:
        movie.ranking = len(movies) - movies.index(movie)

    db.session.commit()

    return render_template("index.html", movies=movies)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = EditForm()

    movie_id = int(request.args.get('movie_id'))
    # Below is true when only request method is POST
    if form.validate_on_submit():
        if update_movie(movie_id, form.rating.data, form.review.data):
            return redirect(url_for('home'))
    return render_template('edit.html', form=form)


@app.route('/select', methods=['GET'])
def select():
    movie_id_api = request.args.get('movie_id_api')

    headers = {
        'Authorization': ACCESS_TOKEN,
        'accept': 'application/json'
    }
    params = {
        'language': 'en-US'
    }

    response = requests.get(url=f'{MOVIE_API_DETAILED_ENDPOINT}{movie_id_api}', params=params, headers=headers)
    response.raise_for_status()
    json_data = response.json()

    title = json_data['original_title']
    path = json_data['poster_path']
    description = json_data['overview']
    year = int(json_data['release_date'].split('-')[0])
    new_movie = add_movie(title, year, description, img_url=f'{MOVIE_POSTER_PATH_PREFIX}{path}')

    movie_id = int(new_movie.id)

    return redirect(url_for('edit', movie_id=movie_id))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        query = form.title.data
        headers = {
            'Authorization': ACCESS_TOKEN,
            'accept': 'application/json'
        }
        params = {
            'query': query,
            'language': 'en-US'
        }

        response = requests.get(url=MOVIE_API_ENDPOINT, params=params, headers=headers)
        response.raise_for_status()
        json_data = response.json()['results']

        return render_template('select.html', movies=json_data)
    return render_template('add.html', form=form)


@app.route('/delete')
def delete():
    movie_id = int(request.args.get('movie_id'))
    delete_movie(movie_id)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
