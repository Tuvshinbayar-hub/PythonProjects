from flask import Flask
import random

app = Flask(__name__)

correct_num = random.randint(0, 9)


def index_decorator(func):
    def wrapper():
        func()
    return wrapper


@app.route('/')
def home():
    return '<h1>Guess Number from 0 to 9</h1>/' \
           '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif"/>'


@app.route('/<int:num>')
def is_higher_or_lower(num):
    if num == correct_num:
        return f'<h1 style="color: green;">You found me</h1>/' \
               f'<img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"/>'
    elif num > correct_num:
        return f'<h1 style="color: purple;">Too high, try again!</h1>/' \
               f'<img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"/>'
    else:
        return f'<h1 style="color: red">Too low, try again!</h1>/' \
               f'<img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"/>'


if __name__ == '__main__':
    app.run(debug=True)
