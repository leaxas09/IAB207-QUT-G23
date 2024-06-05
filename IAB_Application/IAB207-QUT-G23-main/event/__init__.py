from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

eventbp = Blueprint('event', __name__, url_prefix='/event')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'somerandomvalue'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventsdb.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from event.views import main_blueprint, event_blueprint  # Import blueprints here

    app.register_blueprint(main_blueprint, name='main_blueprint')
    app.register_blueprint(event_blueprint, name='event_blueprint')

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", error=e)

    @app.context_processor
    def get_context():
        year = datetime.datetime.today().year
        return dict(year=year)

    return app
