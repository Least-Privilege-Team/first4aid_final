from app.models import User
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


# allows anyone to create a requestor account
class RegistrationForm(FlaskForm):
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
    submit = SubmitField('Register')

    def validate_username(self, username):  # checks for existing username
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username exists, try again.')

    def validate_email(self, email):  # checks for compliant email
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.  Please sign in or recover your password.')


# standard login form for all users
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# allows users to update their own accounts
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=40)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):  # checks for existing username
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken.  Please choose another username.')

    def validate_email(self, email):  # checks for compliant email
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered.  Please sign in or recover your password.')


# allows users to request a password reset
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):  # checks to see if email address is associated with an account
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account exists with that email address.  Please register first.')


# allows users to generate a new password
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')