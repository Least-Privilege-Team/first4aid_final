from flask import Blueprint, render_template

main = Blueprint('main', __name__)


# takes user to main landing page
@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', title='Home')
