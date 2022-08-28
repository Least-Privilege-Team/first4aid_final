import os
import secrets

from app import mail
from flask import current_app, url_for
from flask_mail import Message
from PIL import Image


# allows users to upload picture
def save_picture(form_picture):
    generated_hex = secrets.token_hex(8)  # generates a random hex string
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_filename = generated_hex + f_ext  # appends filename extension
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_filename)   # location to store file

    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)

    image.save(pic_path)

    return pic_filename

# sends the password reset token and message
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='First4Aid Password Reset',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, then ignore this email and no changes will be made.
    '''
    mail.send(msg)
