from app import db
from app.cases.forms import CaseForm
from app.models import Case
from flask import abort, Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required


cases = Blueprint('cases', __name__)


# allows requestors to create new aid requests
@cases.route("/case/new", methods=['GET', 'POST'])
@login_required
def new_case():
    form = CaseForm()
    if form.validate_on_submit():
        case = Case(request_type=form.request_type.data.id, description=form.description.data,
                    requestor_id=current_user.id)
        db.session.add(case)
        db.session.commit()
        flash('Your case has been submitted.', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_case_request.html', title='New Case Request', form=form,
                           legend='New Case Request')


# allows requestors to access existing aid requests
@cases.route("/case/<int:case_id>")
def case(case_id):
    case = Case.query.get_or_404(case_id)
    if case.requestor != current_user:  # verify current user is requestor
        abort(403)
    case = Case.query.get_or_404(case_id)
    return render_template('case.html', request_type=case.request_type, case=case)


# allows requestors to update their own aid requests
@cases.route("/case/<int:case_id>/update", methods=['GET', 'POST'])
@login_required
def update_case(case_id):
    case = Case.query.get_or_404(case_id)
    if case.requestor != current_user:  # verify current user is requestor
        abort(403)
    form = CaseForm()
    if form.validate_on_submit():
        case.request_type = form.request_type.data.id
        case.description = form.description.data
        db.session.commit()
        flash('Case updated successfully.', 'success')
        return redirect(url_for('cases.case', case_id=case.id))
    elif request.method == 'GET':
        form.request_type.data = case.case_type
        form.description.data = case.description
    return render_template('update_case.html', title='Update Case',
                           form=form, legend='Update Case')


# allow requestor to delete their own cases
@cases.route("/case/<int:case_id>/delete", methods=['POST'])
@login_required
def delete_case(case_id):
    case = Case.query.get_or_404(case_id)
    if case.requestor != current_user:  # verify current user is requestor
        abort(403)
    db.session.delete(case)
    db.session.commit()
    flash('Case successfully deleted.', 'success')
    return redirect(url_for('main.home'))

