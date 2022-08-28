"""
Design patterns and application structure was guided by the following sources:

Flask Project Layout Tutorial
(https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/)

Corey Schafer's Flask Tutorial
https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH

Hackers and Slackers Flask Blueprints
https://hackersandslackers.com/flask-blueprints/
"""
import os
from app.config import Config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # instantiates SQLAlchemy, the ORM
bcrypt = Bcrypt()  # used to hash/salt data
login_manager = LoginManager()  # module enables authentication and authorisation
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()  # used for password reset and MFA


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # separates config variables for easier customisation

    # Generate CSRF token
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

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