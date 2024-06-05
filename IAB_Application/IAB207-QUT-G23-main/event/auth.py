from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

# Create a blueprint
authbp = Blueprint('auth', __name__)

# Initialize LoginManager
login_manager = LoginManager()

# User loader function to retrieve a user by their ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    # The validation of form is fine, HTTP request is POST
    if register_form.validate_on_submit():
        # Get username, password, and email from the form
        uname = register_form.user_name.data
        pwd = register_form.password.data
        email = register_form.email_id.data  # Corrected attribute name
        # Check if a user exists
        user = User.query.filter_by(name=uname).first()
        if user:
            flash('Username already exists, please try another')
            return redirect(url_for('auth.register'))
        # Don't store the password in plaintext!
        pwd_hash = generate_password_hash(pwd)
        # Create a new User model object
        new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
        db.session.add(new_user)
        db.session.commit()
        # Commit to the database and redirect to HTML page
        return redirect(url_for('main_blueprint.index'))
    # The else is called when the HTTP request calling this page is a GET
    else:
        return render_template('user.html', form=register_form, heading='Register')


@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        # Get the username and password from the database
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = User.query.filter_by(name=user_name).first()
        # If there is no user with that name
        if user is None:
            error = 'Incorrect username'  # Could be a security risk to give this much info away
        # Check the password - notice password hash function
        elif not check_password_hash(user.password_hash, password):  # Takes the hash and password
            error = 'Incorrect password'
        if error is None:
            # All good, set the login_user of flask_login to manage the user
            login_user(user)
            return redirect(url_for('main_blueprint.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_blueprint.index'))
