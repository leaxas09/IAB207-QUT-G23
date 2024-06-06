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
    if register_form.validate_on_submit():
        uname = register_form.user_name.data
        pwd = register_form.password.data
        email = register_form.email_id.data
        address_id = register_form.address_id.data
        contact_id = register_form.contact_id.data

        user = User.query.filter_by(name=uname).first()
        if user:
            flash('Username already exists, please try another')
            return redirect(url_for('auth.register'))

        pwd_hash = generate_password_hash(pwd)
        new_user = User(
            name=uname,
            password_hash=pwd_hash,
            emailid=email,
            address_id=address_id,  # Use address_id
            contact_id=contact_id  # Use contact_id
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main_blueprint.index'))
    else:
        return render_template('register.html', form=register_form, heading='Register')




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
    return render_template('register.html', form=login_form, heading='Login')

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_blueprint.index'))
