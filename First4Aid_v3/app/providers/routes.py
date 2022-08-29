from flask import Blueprint, flash, redirect, render_template, request, url_for
from app import bcrypt
from ..models import db
from app import logging
from app.providers.forms import CreateProviderAccount, UpdateCaseForm
from app.models import Case, User
from flask_login import current_user, login_required


providers = Blueprint('providers', __name__)


# allow admins to create accounts
@providers.route("/provider/create_account", methods=['GET', 'POST'])
@login_required
def create_account():
    logging.info('Processing default request')
    if current_user.role.role_name == 'Admin':  # validate admin privileges
        form = CreateProviderAccount()
        if form.validate_on_submit():  # hashes password upon submission
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        email=form.email.data, password=hashed_password, role=form.role.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account Created.', 'success')
            return redirect(url_for('providers.portal'))
        return render_template('create_provider_account.html', title='Create Provider Account', form=form)
    else:
        flash(f'Admin access required. Your role is {current_user.role}.', 'danger')
        return redirect(url_for('main.home'))


# list all cases for admins
@providers.route("/provider/admin_cases")
@login_required
def admin_cases():
    logging.info('Processing default request')
    if current_user.role.role_name == 'Admin':  # validate admin privileges
        page = request.args.get('page', 1, type=int)
        cases = Case.query.order_by(Case.date_open)\
            .paginate(page=page, per_page=10)
        return render_template('admin_cases.html', cases=cases)
    else:
        flash(f'Admin access required. Your role is {current_user.role}.', 'danger')
        return redirect(url_for('main.home'))


# gives assigned providers and admins ability to view case details
@providers.route("/provider/case/<int:case_id>")
@login_required
def case_details(case_id):
    logging.info('Processing default request')
    if current_user.role.role_name != 'Requestor':
        case = Case.query.get_or_404(case_id)
        if case.provider == current_user or current_user.role.role_name == 'Admin':  # checks if admin/assigned provider
            return render_template('case_details.html', request_type=case.request_type, case=case)
        else:
            flash('Access not granted to this case.', 'danger')
            return redirect(url_for('providers.portal'))
    else:
        flash('Provider access required', 'danger')
        return redirect(url_for('main.home'))


# gives assigned providers and admins ability to edit case details
@providers.route("/provider/case/update/<int:case_id>", methods=['GET', 'POST'])
@login_required
def update_case(case_id):
    logging.info('Processing default request')
    case = Case.query.get_or_404(case_id)
    if current_user.role.role_name == 'Admin' or case.provider == current_user:  # checks if admin or assigned provider
        form = UpdateCaseForm()
        if form.validate_on_submit():  # assigns form values to data objects
            case.request_type = form.request_type.data.id
            case.description = form.description.data
            case.provider_id = form.provider_select.data.id
            case.status = form.status.data
            case.response = form.response.data
            case.activity_log = form.activity_log.data
            db.session.commit()
            flash('Case updated successfully.', 'success')
            return redirect(url_for('providers.case_details', case_id=case.id))
        elif request.method == 'GET':  # populates form with existing data
            form.request_type.data = case.case_type
            form.description.data = case.description
            form.provider_select.data = case.provider
            form.status.data = case.status
            form.response.data = case.response
            form.activity_log.data = case.activity_log
        return render_template('provider_update_case.html', title='Update Case',
                               form=form, legend='Update Case')
    else:
        flash('Access not granted to this case.', 'danger')
        return redirect(url_for('main.home'))


# lists a provider's assigned cases
@providers.route("/provider/<string:username>")
@login_required
def provider_cases(username):
    logging.info('Processing default request')
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:
        page = request.args.get('page', 1, type=int)

        cases = Case.query.filter_by(provider=user)\
            .order_by(Case.date_open)\
            .paginate(page=page, per_page=5)
        return render_template('provider_cases.html', cases=cases, user=user)
    else:
        flash(f'Provider access required.', 'danger')
        return redirect(url_for('main.home'))


# landing page for providers
@providers.route("/provider/")
@providers.route("/provider/portal")
@login_required
def portal():
    logging.info('Processing default request')
    return render_template('provider_portal.html', title='Provider Portal')
