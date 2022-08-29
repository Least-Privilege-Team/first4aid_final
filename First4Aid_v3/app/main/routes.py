from flask import Blueprint, render_template
from app import logging
main = Blueprint('main', __name__)


# takes user to main landing page
@main.route("/")
@main.route("/home")
def home():
    logging.info('Processing default request')
    return render_template('home.html', title='Home')
