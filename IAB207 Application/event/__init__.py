from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Use Bootstrap for UI
    Bootstrap5(app)

    # Bcrypt for password hashing
    Bcrypt(app)

    # Secret key for session management
    app.secret_key = 'somerandomvalue'

    # Configure and initialize the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventimagedb.sqlite'
    db.init_app(app)

    # Configure upload folder for images
    UPLOAD_FOLDER = 'event/static/image'  # Adjusted to images folder
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # User loader function for login manager
    from .models import User  # Importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from event.views import main_blueprint, event_blueprint  # Import blueprints here

    app.register_blueprint(main_blueprint, name='main_blueprint')
    app.register_blueprint(event_blueprint, name='event_blueprint')




    # Custom error handler
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", error=e)

    # Add a context processor for common template variables
    @app.context_processor
    def get_context():
        year = datetime.datetime.today().year
        return dict(year=year)

    return app
