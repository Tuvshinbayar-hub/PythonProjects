from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
db = SQLAlchemy()
db.init_app(app)

all_books = []


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


def add_book(title: str, author: str, rating: float):
    global db
    new_book = Book(title=title, author=author, rating=rating)
    try:
        db.session.add(new_book)
        db.session.commit()
        print('adding succeeded')
        return True
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print('adding failed')
        return False


def update_book(book_id: int, rating: float):
    global db
    try:
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = rating
        db.session.commit()
        print('update succeeded')
        return True
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print('update failed')
        return False


def delete_book(book_id: int):
    global db
    try:
        book_to_delete = db.get_or_404(Book, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        print('delete succeeded')
        return True
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print('delete failed')
        return False

def get_all_books():
    global all_books
    all_books = Book.query.all()


@app.route('/')
def home():
    get_all_books()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = {}
        for data in request.form.items():
            new_book[data[0]] = data[1]

        if add_book(new_book['title'], new_book['author'], float(new_book['rating'])):
            all_books.append(new_book)
        return redirect('home')

    return render_template('add.html')


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    global all_books
    if request.method == 'POST':
        new_rating = float(request.form.get('rating'))
        update_book(book_id, new_rating)
        return redirect(url_for('home'))
    return render_template('edit.html', book=all_books[book_id-1])


@app.route('/delete/<int:book_id>')
def delete(book_id):
    global all_books
    if delete_book(book_id):
        all_books.pop(book_id-1)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

