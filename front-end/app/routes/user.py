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
from flask import request
from flask import render_template

from app.utilities import forms

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route("/request-support", methods=['GET', 'POST'])
def request_support():
    """Renders the index page of the cake sales section of
    the application. The route is accessed by typing the URL
    /sales/cakes. The route is accessed by GET requests. In the interest
    of keeping the application simple, the route contains all of the
    logic required to retrieve, organise and display the data from the
    database.
    """
    form = forms.CaseForm()

    if request.method == 'GET':
        aid_list = ["Stuff","More Stuff"]
        return render_template(
            'user/request_support_form.html.jinja',
            page_title='New Request',
            form=form,
            aid_list=aid_list)
    elif request.method == 'POST':
        pass

@bp.route("/track-request", methods=['GET'])
def track_request():
    """Renders the index page of the cake sales section of
    the application. The route is accessed by typing the URL
    /sales/cakes. The route is accessed by GET requests. In the interest
    of keeping the application simple, the route contains all of the
    logic required to retrieve, organise and display the data from the
    database.
    """

    return render_template(
        'user/track_request.html.jinja',
        page_title='Welcome to First4Aid')