from app import db, bcrypt
from app.models import Case, User
from app.users.forms import (LoginForm, RegistrationForm, RequestResetForm,
                                      ResetPasswordForm, UpdateAccountForm)
from app.users.utils import save_picture, send_reset_email
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user


users = Blueprint('users', __name__)


# allows users to create a requestor account
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # checks to see if user is already logged in
        flash('Already logged in.', 'success')
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():  # hashes password upon submission
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                         email=form.email.data, password=hashed_password)
        db.session.add(user)  # stages data object for input to DB
        db.session.commit()  # commits new record to DB
        flash(f'Account Created. You may now log in.', 'success')
        return redirect(url_for('users.login'))  # sends user back to login screen
    return render_template('register.html', title='Register', form=form)


# process for logging in all account types
@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:  # checks to see if user is already logged in
        flash('Already logged in.', 'success')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # searches for email in user table
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # matches hashed password
            login_user(user, remember=form.remember.data)  # allows user to stay logged in (can be disabled)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please try again.', 'danger')
    return render_template('login.html', title='Login', form=form)


# closes session
@users.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


# allows users to update their own account information
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)  # pulls function from utils.py
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


# allows requestors to view a list of their own cases
@users.route("/user/<string:username>")
def user_cases(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    cases = Case.query.filter_by(requestor=user)\
        .order_by(Case.date_open.asc())\
        .paginate(page=page, per_page=5)  # matches cases with current user
    return render_template('user_cases.html', cases=cases, user=user)


# allows users to request their own password resets
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # validates email is a registered user
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


# authenticates user's reset token to enable password reset
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated.  You are now able to log in.', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password', form=form)