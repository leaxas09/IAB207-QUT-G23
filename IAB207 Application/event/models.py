from datetime import datetime
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    address_id = db.Column(db.String(255), nullable=True)
    contact_id = db.Column(db.String(20), nullable=True)
    comments = db.relationship('Comment', backref='user')
    purchases = db.relationship('Purchase', backref='user')



    def __repr__(self):
        return f"Name: {self.name}"
    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    ticket_amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500))
    image = db.Column(db.String(120), nullable=True)
    comments = db.relationship('Comment', backref='eventimage')
	# string print method
    def __repr__(self):
        return f"Name: {self.name}"

    def __repr__(self):
        return f"Event: {self.description}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'time': self.time.strftime('%H:%M:%S'),
            'date': self.date.strftime('%Y-%m-%d'),
            'ticket_price': self.ticket_price,
            'ticket_amount': self.ticket_amount,
            'description': self.description,
            'image': self.image  # Include the image in the dictionary
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"

class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    purchase_date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"Purchase: User ID {self.user_id}, Event ID {self.event_id}, Date {self.purchase_date}"
