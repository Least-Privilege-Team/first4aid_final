"""This module contains the routes for the sales portion of the 
application. The module provides an abstraction layer between the
application backend and the frontend. The module also provides a way to
access the database through the database object.

The module imports the following modules from third-party
libraries:
    - flask

The module also imports the models module from the app directory.
"""
from flask import Blueprint
from flask import render_template

bp = Blueprint('index', __name__, url_prefix='')

@bp.route("/", methods=['GET'])
def index():
    """Renders the index page of the cake sales section of
    the application. The route is accessed by typing the URL
    /sales/cakes. The route is accessed by GET requests. In the interest
    of keeping the application simple, the route contains all of the
    logic required to retrieve, organise and display the data from the
    database.
    """

    return render_template(
        'home/index.html.jinja',
        page_title='Welcome to First4Aid')