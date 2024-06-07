from flask import Flask, render_template  # Import Flask and render_template from the flask module
from flask_bootstrap import Bootstrap5  # Import Bootstrap5 from the flask_bootstrap module
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy from the flask_sqlalchemy module
from flask_login import LoginManager  # Import LoginManager from the flask_login module
from flask_bcrypt import Bcrypt  # Import Bcrypt from the flask_bcrypt module
import datetime  # Import datetime for date and time operations
import os  # Import os for operating system dependent functionality

db = SQLAlchemy()  # Initialize SQLAlchemy object

def create_app():
    app = Flask(__name__)  # Create an instance of the Flask application

    # Use Bootstrap for UI
    Bootstrap5(app)  # Initialize Bootstrap5 with the app

    # Bcrypt for password hashing
    Bcrypt(app)  # Initialize Bcrypt with the app

    # Secret key for session management
    app.secret_key = 'somerandomvalue'  # Set the secret key for session management

    # Configure and initialize the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventimagedb.sqlite'  # Set the database URI
    db.init_app(app)  # Initialize the database with the app

    # Configure upload folder for images
    UPLOAD_FOLDER = 'event/static/image'  # Define the upload folder path
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Set the upload folder in the app configuration

    # Initialize the login manager
    login_manager = LoginManager()  # Create an instance of LoginManager
    login_manager.login_view = 'auth.login'  # Set the login view
    login_manager.init_app(app)  # Initialize the login manager with the app

    # User loader function for login manager
    from .models import User  # Import User model to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Load the user by ID

    from event.views import main_blueprint, event_blueprint  # Import blueprints

    app.register_blueprint(main_blueprint, name='main_blueprint')  # Register the main blueprint
    app.register_blueprint(event_blueprint, name='event_blueprint')  # Register the event blueprint

    # Custom error handler
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", error=e)  # Render the 404 error page

    # Add a context processor for common template variables
    @app.context_processor
    def get_context():
        year = datetime.datetime.today().year  # Get the current year
        return dict(year=year)  # Return the year in the context dictionary

    return app  # Return the Flask app instance
