"""
Design patterns and application structure was guided by the following sources:

Flask Project Layout Tutorial
(https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/)

Corey Schafer's Flask Tutorial
https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH

Hackers and Slackers Flask Blueprints
https://hackersandslackers.com/flask-blueprints/
"""
import logging
import os
from app.config import Config
from flask import Flask
from flask_bcrypt import Bcrypt
from .models import login_manager
from flask_mail import Mail
from .models import db

bcrypt = Bcrypt()  # used to hash/salt data
mail = Mail()  # used for password reset and MFA

# Enable logging
logging.basicConfig(filename='app-first4aid_v3.log', level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # separates config variables for easier customisation

    # Generate CSRF token
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # Register database functions with the Flask app.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # configure blueprints for design modularity
    from app.users.routes import users
    from app.cases.routes import cases
    from app.main.routes import main
    from app.providers.routes import providers

    app.register_blueprint(users)
    app.register_blueprint(cases)
    app.register_blueprint(main)
    app.register_blueprint(providers)

    return app