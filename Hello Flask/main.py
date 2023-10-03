# from flask import Flask
#
# app = Flask(__name__)
#
#
# def make_bold(func):
#     def wrapper():
#         decorated = f'<b>{func()}</b>'
#         return decorated
#     return wrapper
#
#
# def make_emphasis(func):
#     def wrapper():
#         decorated = f'<em>{func()}</em>'
#         return decorated
#     return wrapper
#
#
# def make_underlined(func):
#     def wrapper():
#         return f'<u>{func()}</u>'
#     return wrapper
#
#
# @app.route('/')
# @make_bold
# @make_emphasis
# @make_underlined
# def greet():
#     return 'Hello World'
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

# Create the logging_decorator() function 👇
def logging_decorator(function):
    def wrapper(*args):
        return function(*args)
    return wrapper


# Use the decorator 👇
@logging_decorator
def find_sum(*args):
    sums = 0
    for arg in args:
        sums += int(arg)
    return sums


result = find_sum(1, 2, 3)
print(result)
