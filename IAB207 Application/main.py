from event import create_app  # Import the create_app function from the event module
from event.models import db  # Import the db object from the event.models module
from event.auth import login_manager  # Import the login_manager from the event.auth module
from event.views import main_blueprint, event_blueprint  # Import the blueprints from the event.views module

app = create_app()  # Create an instance of the Flask application
login_manager.init_app(app)  # Initialize the login manager with the app instance
app.register_blueprint(main_blueprint)  # Register the main blueprint with the app
app.register_blueprint(event_blueprint)  # Register the event blueprint with the app

if __name__ == '__main__':  # If this script is run directly, execute the following block
    with app.app_context():  # Push the application context to interact with the database
        try:
            db.create_all()  # Create all database tables
        except Exception as e:  # Catch any exceptions that occur during table creation
            print(f"An error occurred while creating database tables: {e}")  # Print the error message
    app.run(debug=True, port=5002)  # Run the Flask application with debug mode enabled on port 5002
