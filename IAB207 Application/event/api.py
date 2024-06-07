from flask import Blueprint, jsonify, request  # Import necessary modules from Flask
from .models import db, Event  # Import the database object and the Event model

api_bp = Blueprint('api', __name__, url_prefix='/api')  # Create a new Blueprint for API routes

# Get all events
@api_bp.route('/events', methods=['GET'])  # Define a route for getting all events
def get_events():
    events = db.session.scalars(db.select(Event)).all()  # Query all events from the database
    events_list = [event.to_dict() for event in events]  # Convert each event to a dictionary
    return jsonify(events=events_list)  # Return the events as a JSON response

# Create a new event
@api_bp.route('/events', methods=['POST'])  # Define a route for creating a new event
def create_event():
    json_dict = request.get_json()  # Get the JSON data from the request
    if not json_dict:  # Check if the JSON data is provided
        return jsonify(message="No input data provided!"), 400  # Return an error message if no data is provided

    event = Event(  # Create a new Event object with the provided data
        location=json_dict['location'],
        time=json_dict['time'],
        date=json_dict['date'],
        ticket_price=json_dict['ticket_price'],
        ticket_amount=json_dict['ticket_amount'],
        description=json_dict['description']
    )
    db.session.add(event)  # Add the new event to the database session
    db.session.commit()  # Commit the session to save the event in the database
    return jsonify(message='Successfully created new event!'), 201  # Return a success message

# Delete an existing event
@api_bp.route('/events/<int:event_id>', methods=['DELETE'])  # Define a route for deleting an event by ID
def delete_event(event_id):
    event = db.session.scalar(db.select(Event).where(Event.id == event_id))  # Query the event by ID
    if event:  # Check if the event exists
        db.session.delete(event)  # Delete the event from the database session
        db.session.commit()  # Commit the session to remove the event from the database
        return jsonify(message='Record deleted!'), 200  # Return a success message
    else:
        return jsonify(message='Event not found!'), 404  # Return an error message if the event is not found

# Update an existing event
@api_bp.route('/events/<int:event_id>', methods=['PUT'])  # Define a route for updating an event by ID
def update_event(event_id):
    json_dict = request.get_json()  # Get the JSON data from the request
    event = db.session.scalar(db.select(Event).where(Event.id == event_id))  # Query the event by ID
    if event:  # Check if the event exists
        event.location = json_dict['location']  # Update the event's location
        event.time = json_dict['time']  # Update the event's time
        event.date = json_dict['date']  # Update the event's date
        event.ticket_price = json_dict['ticket_price']  # Update the event's ticket price
        event.ticket_amount = json_dict['ticket_amount']  # Update the event's ticket amount
        event.description = json_dict['description']  # Update the event's description
        db.session.commit()  # Commit the session to save the updates in the database
        return jsonify(message='Record updated!'), 200  # Return a success message
    else:
        return jsonify(message='Event not found!'), 404  # Return an error message if the event is not found

# Add to_dict method to Event model
def event_to_dict(event):  # Define a function to convert an Event object to a dictionary
    return {
        'id': event.id,
        'location': event.location,
        'time': event.time.strftime('%H:%M:%S'),  # Format the time as a string
        'date': event.date.strftime('%Y-%m-%d'),  # Format the date as a string
        'ticket_price': event.ticket_price,
        'ticket_amount': event.ticket_amount,
        'description': event.description
    }

# Update Event model to include to_dict method
Event.to_dict = event_to_dict  # Add the to_dict method to the Event model
