from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
# from wtforms_sqlalchemy.fields import QuerySelectField


class CaseForm(FlaskForm):
    request_type = StringField('Select Type of Aid Requested', validators=[DataRequired()])  # REVISIT: make drop-down
    description = TextAreaField('Please describe your situation', validators=[DataRequired()])
    submit = SubmitField('Submit')