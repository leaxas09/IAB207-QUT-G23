from flask import Blueprint, render_template, redirect, url_for, flash  # Import necessary modules from Flask
from .forms import LoginForm, RegisterForm  # Import the login and registration forms
from flask_login import LoginManager, login_user, login_required, logout_user  # Import Flask-Login functions
from flask_bcrypt import generate_password_hash, check_password_hash  # Import Bcrypt for password hashing
from .models import User  # Import the User model
from . import db  # Import the database object

# Create a blueprint for authentication routes
authbp = Blueprint('auth', __name__)

# Initialize LoginManager
login_manager = LoginManager()

# User loader function to retrieve a user by their ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Query the user by ID

@authbp.route('/register', methods=['GET', 'POST'])  # Define a route for user registration
def register():
    register_form = RegisterForm()  # Instantiate the registration form
    if register_form.validate_on_submit():  # Check if the form is submitted and valid
        uname = register_form.user_name.data  # Get the username from the form
        pwd = register_form.password.data  # Get the password from the form
        email = register_form.email_id.data  # Get the email from the form
        address_id = register_form.address_id.data  # Get the address ID from the form
        contact_id = register_form.contact_id.data  # Get the contact ID from the form

        user = User.query.filter_by(name=uname).first()  # Check if the username already exists
        if user:  # If the user exists, flash a message and redirect to the registration page
            flash('Username already exists, please try another')
            return redirect(url_for('auth.register'))

        pwd_hash = generate_password_hash(pwd)  # Hash the password
        new_user = User(  # Create a new User object
            name=uname,
            password_hash=pwd_hash,
            emailid=email,
            address_id=address_id,  # Set the address ID
            contact_id=contact_id  # Set the contact ID
        )
        db.session.add(new_user)  # Add the new user to the database session
        db.session.commit()  # Commit the session to save the user in the database

        return redirect(url_for('main_blueprint.index'))  # Redirect to the index page of the main blueprint
    else:
        return render_template('register.html', form=register_form, heading='Register')  # Render the registration template

@authbp.route('/login', methods=['GET', 'POST'])  # Define a route for user login
def login():
    login_form = LoginForm()  # Instantiate the login form
    error = None  # Initialize error message variable
    if login_form.validate_on_submit():  # Check if the form is submitted and valid
        user_name = login_form.user_name.data  # Get the username from the form
        password = login_form.password.data  # Get the password from the form
        user = User.query.filter_by(name=user_name).first()  # Query the user by username
        if user is None:  # If the user does not exist
            error = 'Incorrect username'  # Set an error message
        elif not check_password_hash(user.password_hash, password):  # Check if the password is correct
            error = 'Incorrect password'  # Set an error message
        if error is None:  # If no errors, log the user in
            login_user(user)  # Log the user in using Flask-Login
            return redirect(url_for('main_blueprint.index'))  # Redirect to the index page of the main blueprint
        else:
            flash(error)  # Flash the error message
    return render_template('register.html', form=login_form, heading='Login')  # Render the login template

@authbp.route('/logout')  # Define a route for user logout
@login_required  # Ensure the user is logged in to access this route
def logout():
    logout_user()  # Log the user out using Flask-Login
    return redirect(url_for('main_blueprint.index'))  # Redirect to the index page of the main blueprint
