from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return "Hello World"

@views.route('/bye')
def bye():
    return "Bye World"
