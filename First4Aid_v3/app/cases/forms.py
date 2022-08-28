from app.models import Aid
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

import wtforms_sqlalchemy  # seems like a superfluous import; however, application failed to run without it
from wtforms_sqlalchemy.fields import QuerySelectField


def request_choices():  # creates list options for aid request select field
    return Aid.query.all()


class CaseForm(FlaskForm):  # creates default case form for users
    request_type = QuerySelectField(query_factory=request_choices, allow_blank=True, get_label='aid_type',
                                    validators=[DataRequired()])
    description = TextAreaField('Please describe your situation', validators=[DataRequired()])
    submit = SubmitField('Submit')
