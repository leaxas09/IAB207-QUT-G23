from datetime import datetime  # Import datetime for date and time operations
from flask_login import UserMixin  # Import UserMixin for user session management with Flask-Login
from . import db  # Import the database object
from werkzeug.security import generate_password_hash, check_password_hash  # Import password hashing and checking functions

# User model
class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    name = db.Column(db.String(100), index=True, nullable=False)  # User name column
    emailid = db.Column(db.String(100), index=True, nullable=False)  # User email column
    password_hash = db.Column(db.String(255), nullable=False)  # Password hash column
    address_id = db.Column(db.String(255), nullable=True)  # Address ID column (optional)
    contact_id = db.Column(db.String(20), nullable=True)  # Contact ID column (optional)
    comments = db.relationship('Comment', backref='user')  # Relationship to Comment model
    purchases = db.relationship('Purchase', backref='user')  # Relationship to Purchase model

    def __repr__(self):
        return f"Name: {self.name}"  # String representation of the User object

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # Set password hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Check password against stored hash

# Event model
class Event(db.Model):
    __tablename__ = 'events'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    name = db.Column(db.String(200), nullable=False)  # Event name column
    location = db.Column(db.String(200), nullable=False)  # Event location column
    time = db.Column(db.Time, nullable=False)  # Event time column
    date = db.Column(db.Date, nullable=False)  # Event date column
    ticket_price = db.Column(db.Float, nullable=False)  # Ticket price column
    ticket_amount = db.Column(db.Integer, nullable=False)  # Ticket amount column
    genre = db.Column(db.String(100))  # Genre column (optional)
    description = db.Column(db.String(500))  # Description column (optional)
    image = db.Column(db.String(120), nullable=True)  # Image column (optional)
    comments = db.relationship('Comment', backref='eventimage')  # Relationship to Comment model

    def __repr__(self):
        return f"Event: {self.description}"  # String representation of the Event object

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'time': self.time.strftime('%H:%M:%S'),  # Format time to string
            'date': self.date.strftime('%Y-%m-%d'),  # Format date to string
            'ticket_price': self.ticket_price,
            'ticket_amount': self.ticket_amount,
            'description': self.description,
            'image': self.image  # Include the image in the dictionary
        }

# Comment model
class Comment(db.Model):
    __tablename__ = 'comments'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    text = db.Column(db.String(400))  # Comment text column
    created_at = db.Column(db.DateTime, default=datetime.now())  # Timestamp for when the comment was created
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key to User model
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))  # Foreign key to Event model

    def __repr__(self):
        return f"Comment: {self.text}"  # String representation of the Comment object

# Purchase model
class Purchase(db.Model):
    __tablename__ = 'purchases'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key to User model
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))  # Foreign key to Event model
    purchase_date = db.Column(db.DateTime, default=datetime.now())  # Timestamp for when the purchase was made

    def __repr__(self):
        return f"Purchase: User ID {self.user_id}, Event ID {self.event_id}, Date {self.purchase_date}"  # String representation of the Purchase object
