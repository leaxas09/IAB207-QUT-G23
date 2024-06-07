from flask_wtf import FlaskForm  # Import FlaskForm from flask_wtf
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, FloatField, IntegerField, BooleanField  # Import necessary fields from wtforms
from wtforms.validators import InputRequired, EqualTo, Regexp, ValidationError, Email  # Import validators from wtforms
from wtforms.validators import Email as EmailValidator  # Import Email validator with alias to avoid conflict
from flask_wtf.file import FileRequired, FileField, FileAllowed  # Import file handling validators from flask_wtf.file
from .models import User  # Import the User model

# Allowed file extensions for file upload
ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Create new event form
class CreateEventForm(FlaskForm):
    location = StringField('Location', validators=[InputRequired()])  # Location field with InputRequired validator
    date = StringField('Date', validators=[InputRequired()])  # Date field with InputRequired validator
    time = StringField('Time', validators=[InputRequired()])  # Time field with InputRequired validator
    ticket_price = FloatField('Ticket Price', validators=[InputRequired()])  # Ticket price field with InputRequired validator
    ticket_amount = IntegerField('Ticket Amount', validators=[InputRequired()])  # Ticket amount field with InputRequired validator
    description = TextAreaField('Description', validators=[InputRequired()])  # Description field with InputRequired validator
    image = FileField('Destination Image', validators=[  # Image file field with validators for required file and allowed file types
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    submit = SubmitField('Create Event')  # Submit button

# User login form
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])  # Username field with InputRequired validator
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])  # Password field with InputRequired validator
    remember_me = BooleanField("Remember me")  # Remember me checkbox field
    submit = SubmitField("Login")  # Submit button

# User registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])  # Username field with InputRequired validator
    email_id = StringField("Email Address", validators=[InputRequired("Please enter an email"), Email()])  # Email field with InputRequired and Email validators
    address_id = StringField("Address", validators=[InputRequired("Please enter a valid address")])  # Address field with InputRequired validator
    contact_id = StringField("Contact Number", validators=[  # Contact number field with InputRequired and Regexp validators
        InputRequired("Please enter a contact number"),
        Regexp('^\d+$', message="Contact number must contain only numbers")
    ])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])  # Password field with InputRequired and EqualTo validators
    confirm = PasswordField("Confirm Password")  # Confirm password field
    submit = SubmitField("Register")  # Submit button

    def validate_email_id(self, email_id):  # Custom validator for email field
        user = User.query.filter_by(emailid=email_id.data).first()  # Query the user by email
        if user:  # If user exists, raise a ValidationError
            raise ValidationError('Email already registered. Please use a different email address.')

# User comment form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])  # Comment text field with InputRequired validator
    submit = SubmitField('Create')  # Submit button
