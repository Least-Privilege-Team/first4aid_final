from app.models import Aid, Role, Status, User
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

import wtforms_sqlalchemy  # seems like a superfluous import, but app fails to run without it
from wtforms_sqlalchemy.fields import QuerySelectField


# creates list options for user roles
def role_choices():
    return Role.query.all()


# allows admins to create user accounts and assign roles
class CreateProviderAccount(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=40)])
    last_name = StringField('Last Name',
                             validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    role = QuerySelectField(query_factory=role_choices, allow_blank=True, get_label='role_name',
                                    validators=[DataRequired()])
    submit = SubmitField('Create Provider Account')

    def validate_username(self, username):  # checks for existing username
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username exists, try again.')

    def validate_email(self, email):  # checks for compliant email
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.  Please sign in or recover your password.')


# create list options for aid request types
def request_choices():
    return Aid.query.all()


# create list options for provider assignment
def provider_choices():
    return User.query.all()


# create list options for status assignment
def status_choices():
    return Status.query.all()


# allows providers to update cases
class UpdateCaseForm(FlaskForm):
    request_type = QuerySelectField(query_factory=request_choices, allow_blank=True, get_label='aid_type',
                                    validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    provider_select = QuerySelectField(query_factory=provider_choices, allow_blank=True)
    status = QuerySelectField(query_factory=status_choices, allow_blank=True, get_label='status_name',
                                    validators=[DataRequired()])
    response = TextAreaField('Response Actions Taken')
    activity_log = TextAreaField('Activity Log')
    submit = SubmitField('Save Updates')

