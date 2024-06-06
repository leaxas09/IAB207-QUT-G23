from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, FloatField, IntegerField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Regexp, ValidationError, Email
from wtforms.validators import Email as EmailValidator
from flask_wtf.file import FileRequired, FileField, FileAllowed
from .models import User

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Create new event
class CreateEventForm(FlaskForm):
    location = StringField('Location', validators=[InputRequired()])
    date = StringField('Date', validators=[InputRequired()])
    time = StringField('Time', validators=[InputRequired()])
    ticket_price = FloatField('Ticket Price', validators=[InputRequired()])
    ticket_amount = IntegerField('Ticket Amount', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Destination Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    submit = SubmitField('Create Event')

# User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    remember_me = BooleanField("Remember me")  # Add the remember_me field
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[InputRequired("Please enter an email"), Email()])
    address_id = StringField("Address", validators=[InputRequired("Please enter a valid address")])
    contact_id = StringField("Contact Number", validators=[
        InputRequired("Please enter a contact number"),
        Regexp('^\d+$', message="Contact number must contain only numbers")
    ])

    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

    def validate_email_id(self, email_id):
        user = User.query.filter_by(emailid=email_id.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email address.')



# User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')

