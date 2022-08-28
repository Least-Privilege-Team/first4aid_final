"""This module contains the routes for the cases portion of the 
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
from flask import jsonify
import inspect

from ..models import db
from ..models import Case
from ..utilities import db_utilities

bp = Blueprint('cases', __name__, url_prefix='/cases')

@bp.route("", methods=['POST'])
def create_case():
    """Renders the index page of the cake sales section of
    the application. The route is accessed by typing the URL
    /sales/cakes. The route is accessed by GET requests. In the interest
    of keeping the application simple, the route contains all of the
    logic required to retrieve, organise and display the data from the
    database.
    """
    request_data = request.get_json()

    db.session.add(Case(
        id=None,
        requestor_id=request_data['requestor_id'],
        provider_id=None,
        request_type_id=request_data['request_type_id'],
        description=request_data['description'],
        attachments=request_data['attachments'],
        status_id=1,
        response=None,
        date_open=None,
        date_closed=None,
        activity_log=request_data['activity_log']))
    db.session.commit()

    return jsonify([]), 200

@bp.route("", methods=['GET'])
def get_all_cases():
    """Renders the index page of the cake sales section of
    the application. The route is accessed by typing the URL
    /sales/cakes. The route is accessed by GET requests. In the interest
    of keeping the application simple, the route contains all of the
    logic required to retrieve, organise and display the data from the
    database.
    """
    # Organise the data into a list of dictionaries for JSON.
    return jsonify(
        db_utilities.table_data_to_dict(db.session.query(Case).all()))

@bp.route("/<int:case_id>", methods=['GET'])
def get_case_by_id(case_id):
    """Renders the index page of the cake sales section of
    the application. The route is accessed by typing the URL
    /sales/cakes. The route is accessed by GET requests. In the interest
    of keeping the application simple, the route contains all of the
    logic required to retrieve, organise and display the data from the
    database.
    """
    case = db_utilities.table_data_to_dict(
        db.session.query(Case).filter(Case.id==case_id).all())

    # Organise the data into a list of dictionaries for JSON.
    if case:
        return jsonify(case[0])
    else:
        return jsonify([]), 404

@bp.route("/<int:case_id>", methods=['PUT'])
def update_case_by_id(case_id):
    """Renders the index page of the cake sales section of
    the application. The route is accessed by typing the URL
    /sales/cakes. The route is accessed by GET requests. In the interest
    of keeping the application simple, the route contains all of the
    logic required to retrieve, organise and display the data from the
    database.
    """
    request_data = request.get_json()

    case = db.session.query(Case).filter(Case.id==case_id)

    if case.all():
        case.update({
            'requestor_id': request_data['requestor_id'],
            'provider_id': request_data['provider_id'],
            'request_type': request_data['request_type'],
            'description': request_data['description'],
            'attachments': request_data['attachments'],
            'status_id': request_data['status_id'],
            'response': request_data['response'],
            'date_open': request_data['date_open'],
            'date_closed': request_data['date_closed'],
            'activity_log': request_data['activity_log']})
        db.session.commit()
        return jsonify([]), 200
    else:
        return jsonify([]), 404

@bp.route("/<int:case_id>", methods=['DELETE'])
def delete_case_by_id(case_id):
    """Renders the index page of the cake sales section of
    the application. The route is accessed by typing the URL
    /sales/cakes. The route is accessed by GET requests. In the interest
    of keeping the application simple, the route contains all of the
    logic required to retrieve, organise and display the data from the
    database.
    """
    case = db.session.query(Case).filter(Case.id==case_id)

    if case.all():
        case.delete()
        db.session.commit()
        return jsonify([]), 200
    else:
        return jsonify([]), 404