from datetime import datetime
from app import db, login_manager
from flask import current_app
from flask_login import UserMixin
import jwt


@login_manager.user_loader
def load_user(user_id):  # gets user_id for current_user
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):  # class works with login manager to authenticate/authorise user
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False, nullable=False)
    last_name = db.Column(db.String(30), unique=False, nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=1)  # defaults to least privilege
    requests = db.relationship('Case', backref='requestor', foreign_keys='Case.requestor_id', lazy=True)
    assigned_cases = db.relationship('Case', backref='provider', foreign_keys='Case.provider_id', lazy=True)

    def get_reset_token(self):  # function for password reset, sends reset token
        reset_token = jwt.encode(
            {
                "user_id": self.id
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token

    @staticmethod  # validation method does not change between users
    def verify_reset_token(token):  # accepts token for validation, enabling password reset
        try:
            user_id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):  # allows string value to represent object
        return f"{self.last_name}, {self.first_name}, {self.role}, {self.username}"


class Case(db.Model):  # location for requestor data
    id = db.Column(db.Integer, primary_key=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    request_type = db.Column(db.Integer, db.ForeignKey('aid.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False, default=1)
    response = db.Column(db.Text, nullable=True)
    date_open = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_closed = db.Column(db.DateTime, nullable=True)
    activity_log = db.Column(db.Text, nullable=False, default='Case created')

    def __repr__(self):  # allows string value to represent object
        return f"Case #{self.id},{self.request_type},{self.requestor.username}"


class Aid(db.Model):  # stores types of aid available
    id = db.Column(db.Integer, primary_key=True)
    aid_type = db.Column(db.String(30), nullable=False)
    case = db.relationship('Case', backref='case_type', foreign_keys='Case.request_type', lazy=True)

    def __repr__(self):  # allows string value to represent object
        return f"{self.aid_type}"


class Status(db.Model):  # stores types of status
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(30), nullable=False)
    case = db.relationship('Case', backref='status', foreign_keys='Case.status_id', lazy=True)

    def __repr__(self):  # allows string value to represent object
        return f"{self.status_name}"


class Role(db.Model):  # stores types of roles
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(30), nullable=False)
    user = db.relationship('User', backref='role', foreign_keys='User.role_id', lazy=True)

    def __repr__(self):  # allows string value to represent object
        return f"{self.role_name}"
