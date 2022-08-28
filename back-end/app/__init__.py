"""This module initialises the flask application.
"""
import os

from flask import Flask
from flask import redirect
from flask import url_for

from .models import db
#from .db_migration import create_data_after_db_init

def create_app(test_config=None):
    """Create and configure the flask application.
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Register database functions with the Flask app.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()

    # Check if the database contains data. If not, add the data.
    #if db.session.query(models.Statuses).first() is None:
    #    create_data_after_db_init()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Generate CSRF token
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # apply the blueprints to the app
    from .routes import cases

    app.register_blueprint(cases.bp)
    
    return app