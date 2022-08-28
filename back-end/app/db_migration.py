"""This module creates the data for the database. It is called by the
create_app function inside the app directory __init__.py module soon
after a connection with the database is established. This module 
imports the database object and GoblinCakeSales model from the models
module located in the app directory.
"""
import os
from sqlalchemy.sql import func

from flask_bcrypt import generate_password_hash

from .models import db
from .models import Statuses
from .models import RequestTypes
from .models import Requestors
from .models import Providers
from .models import Cases
from .models import CaseActivities
#from .models import Messages

def create_data_after_db_init():
    """This function creates the data for the database."""
    db.session.add(Statuses(id=1, value='New'))
    db.session.add(Statuses(id=2, value='In Progress'))
    db.session.commit()

    db.session.add(RequestTypes(id=1, value='Food'))
    db.session.add(RequestTypes(id=2, value='Evacuation'))
    db.session.add(RequestTypes(id=3, value='Financial'))
    db.session.add(RequestTypes(id=4, value='Medical'))
    db.session.add(RequestTypes(id=5, value='Transport'))
    db.session.commit()

    db.session.add(Requestors(id=1, first_name='John', last_name='Peter',
    email='jpeter5j@gravatar.com'))
    db.session.commit()

    db.session.add(Providers(id=1, first_name='Nora', last_name='Morling',
    email='nmorlingb@canalblog.com',
    password=generate_password_hash('password2022', 10)))
    db.session.commit()

    db.session.add(Cases(id=1, requestor_id=1, provider_id=1,
        request_type_id=1, status_id=1,
        description='Need help with food.',
        response='We will help.'))
    db.session.commit()
    
    db.session.add(CaseActivities(id=1, case_id=1, entry='Created today'))
    db.session.commit()