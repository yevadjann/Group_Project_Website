# Here we will be storing our standard routes
# Blueprint is a bunch of URLs defined
from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return "<h1>Quiz</h1"
