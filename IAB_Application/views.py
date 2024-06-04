from flask import Blueprint, render_template, request, redirect, url_for

from .froms import EventForm
from . import db
# Import your models and other necessary dependencies
from .models import Event, Comment

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    events = Event.query.all()  # Replace with your actual query
    return render_template('index.html', events=events)

@main_bp.route('/event_detail', defaults={'event_id': None})
@main_bp.route('/event_detail/<int:event_id>')
def event_detail(event_id):
    if event_id is not None:
        # Fetch the event data using the event_id
        event = Event.query.get(event_id)
