from event import create_app
from event.models import db
from event.auth import login_manager
from event.views import main_blueprint, event_blueprint  # Updated import statement

app = create_app()
login_manager.init_app(app)
app.register_blueprint(main_blueprint)  # Register the main blueprint
app.register_blueprint(event_blueprint)  # Register the event blueprint

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"An error occurred while creating database tables: {e}")
    app.run(debug=True, port=5002)  # Change port here if needed
