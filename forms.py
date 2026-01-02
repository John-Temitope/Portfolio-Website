from wtforms import StringField, EmailField, TelField, TextAreaField, PasswordField
from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, InputRequired, EqualTo, URL
from flask_ckeditor import CKEditorField


class ContactForm(FlaskForm):
    name = StringField(label="Full Name", validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired()])
    phone = TelField(label="Phone Number", validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class RegisterForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired(), EqualTo("confirm_password", message='Passwords must match')])
    confirm_password = PasswordField(label="Confirm Password")
    submit = SubmitField(label="Register")


class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")


# WTForm for creating a blog post
class CreateProjectPost(FlaskForm):
    title = StringField(label="Project Title", validators=[DataRequired()])
    subtitle = StringField(label="Subtitle", validators=[DataRequired()])
    img_url = StringField(label="Project URL", validators=[DataRequired(), URL()])
    body = CKEditorField(label="Project Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


"""
Note: For production, it's recommended to register for a free API key from TinyMCE Cloud
 and replace no-api-key with your own.
"""