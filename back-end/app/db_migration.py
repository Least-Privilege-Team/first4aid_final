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
from .models import User
from .models import Case
from .models import Aid
from .models import Status
from .models import Role

def create_data_after_db_init():
    """This function creates the data for the database."""
    db.session.add(Role(id=1, role_name='Requestor'))
    db.session.add(Role(id=2, role_name='Provider'))
    db.session.add(Role(id=3, role_name='Admin'))
    db.session.commit()

    db.session.add(Aid(id=1, aid_type='Food'))
    db.session.add(Aid(id=2, aid_type='Evacuation'))
    db.session.add(Aid(id=3, aid_type='Financial'))
    db.session.add(Aid(id=4, aid_type='Medical'))
    db.session.add(Aid(id=5, aid_type='Transport'))
    db.session.commit()
    
    db.session.add(Status(id=1, status_name='Open'))
    db.session.add(Status(id=2, status_name='In Progress'))
    db.session.add(Status(id=3, status_name='Closed'))
    db.session.commit()

    hashed_password = generate_password_hash('password').decode('utf-8')
    db.session.add(User(id=0, first_name='Test', last_name='Admin',
        username='testadmin1', email='testadmin1@abc.com', image_file=None,
        password=hashed_password, role_id=3))
    db.session.commit()