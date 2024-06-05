from flask import Blueprint, jsonify, request
from .models import db, Event

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Get all events
@api_bp.route('/events', methods=['GET'])
def get_events():
    events = db.session.scalars(db.select(Event)).all()
    events_list = [event.to_dict() for event in events]
    return jsonify(events=events_list)

# Create a new event
@api_bp.route('/events', methods=['POST'])
def create_event():
    json_dict = request.get_json()
    if not json_dict:
        return jsonify(message="No input data provided!"), 400

    event = Event(
        location=json_dict['location'],
        time=json_dict['time'],
        date=json_dict['date'],
        ticket_price=json_dict['ticket_price'],
        ticket_amount=json_dict['ticket_amount'],
        description=json_dict['description']
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(message='Successfully created new event!'), 201

# Delete an existing event
@api_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = db.session.scalar(db.select(Event).where(Event.id == event_id))
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify(message='Record deleted!'), 200
    else:
        return jsonify(message='Event not found!'), 404

# Update an existing event
@api_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    json_dict = request.get_json()
    event = db.session.scalar(db.select(Event).where(Event.id == event_id))
    if event:
        event.location = json_dict['location']
        event.time = json_dict['time']
        event.date = json_dict['date']
        event.ticket_price = json_dict['ticket_price']
        event.ticket_amount = json_dict['ticket_amount']
        event.description = json_dict['description']
        db.session.commit()
        return jsonify(message='Record updated!'), 200
    else:
        return jsonify(message='Event not found!'), 404

# Add to_dict method to Event model
def event_to_dict(event):
    return {
        'id': event.id,
        'location': event.location,
        'time': event.time.strftime('%H:%M:%S'),
        'date': event.date.strftime('%Y-%m-%d'),
        'ticket_price': event.ticket_price,
        'ticket_amount': event.ticket_amount,
        'description': event.description
    }

# Update Event model to include to_dict method
Event.to_dict = event_to_dict
