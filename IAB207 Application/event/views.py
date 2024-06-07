from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask import abort
from flask_login import current_user, login_user, logout_user, login_required
from event.models import Event
from event.models import Purchase, Event
from event import db
from .forms import LoginForm, RegisterForm, CommentForm
from .models import User
from .models import Event, Purchase
from .models import Comment
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import sqlite3
from sqlalchemy import or_

main_blueprint = Blueprint('main', __name__)
event_blueprint = Blueprint('event', __name__, url_prefix='/event')

@main_blueprint.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@main_blueprint.route('/search')
def search():
    search_query = request.args.get('search', '')
    if search_query:
        query = f"%{search_query}%"
        events = Event.query.filter(or_( Event.name.ilike(query), Event.genre.ilike(query) )).all()
        num_results = len(events)
        if num_results == 0:
            flash('No results found.', 'warning')
        else:
            flash(f'{num_results} results found.', 'success')
    else:
        events = Event.query.all()

    return render_template('index.html', events=events)

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.user_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Sign In', form=form)

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        uname = register_form.user_name.data
        pwd = register_form.password.data
        email = register_form.email_id.data
        address_id = register_form.address_id.data
        contact_id = register_form.contact_id.data

        user = User.query.filter_by(name=uname).first()
        if user:
            flash('Username already exists, please try another')
        else:
            pwd_hash = generate_password_hash(pwd)
            new_user = User(
                name=uname,
                password_hash=pwd_hash,
                emailid=email,
                address_id=address_id,  # Use address_id
                contact_id=contact_id  # Use contact_id
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful!')
            return redirect(url_for('main_blueprint.index'))

    return render_template('register.html', form=register_form, heading='Register')


@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

from flask import flash, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime

@event_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        time_str = request.form.get('time')
        date_str = request.form.get('date')
        ticket_price = float(request.form.get('ticket_price'))
        ticket_amount = int(request.form.get('ticket_amount'))
        genre = request.form.get('genre')
        description = request.form.get('description')
        image_file = request.files.get('image')

        if image_file:
            filename = secure_filename(image_file.filename)
            # Full path including 'event/static/image'
            image_dir = os.path.join('event', 'static', 'image')
            os.makedirs(image_dir, exist_ok=True)
            image_path = os.path.join(image_dir, filename)
            image_file.save(image_path)
            # Relative path for storing in the database
            relative_image_path = os.path.join('image', filename)
        else:
            relative_image_path = None

        try:
            time_obj = datetime.strptime(time_str, '%H:%M').time()
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid time or date format', 'error')
            return redirect(url_for('event_blueprint.create'))

        event = Event(
            name=name,
            location=location,
            time=time_obj,
            date=date_obj,
            ticket_price=ticket_price,
            ticket_amount=ticket_amount,
            genre=genre,
            description=description,
            image=relative_image_path  # Store the relative path
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully', 'success')
        return redirect(url_for('main_blueprint.index'))

    return render_template('create_event.html')




@event_blueprint.route('/details/<int:event_id>', methods=['GET'])
def details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_details.html', event=event)


@event_blueprint.route('/checkout/<int:event_id>', methods=['POST'])
@login_required
def checkout(event_id): #checkout page
    event = Event.query.get_or_404(event_id)
    ticket_quantity = int(request.form.get('ticket_quantity'))
    ticket_total = ticket_quantity * event.ticket_price
    if ticket_quantity > event.ticket_amount:
        flash('Not enough tickets available.', 'error')
        return redirect(url_for('event_blueprint.details', event_id=event_id))
    return render_template('checkout.html', event=event, ticket_quantity=ticket_quantity, ticket_total=ticket_total)

@event_blueprint.route('/confirm_purchase/<int:event_id>', methods=['POST'])
@login_required
def confirm_purchase(event_id):
    event = Event.query.get_or_404(event_id)
    ticket_quantity = int(request.form.get('ticket_quantity'))
    if ticket_quantity > event.ticket_amount:
        flash('Not enough tickets available.', 'error')
        return redirect(url_for('event.details', event_id=event_id))

    ticket_result = event.ticket_amount - ticket_quantity

    event.ticket_amount = ticket_result
    db.session.commit()

    for _ in range(ticket_quantity):
        purchase_ticket = Purchase(user_id=current_user.id, event_id=event.id)
        db.session.add(purchase_ticket)

    db.session.commit()

    tickets = Purchase.query\
        .filter(Purchase.user_id == current_user.id, Purchase.event_id == event_id)\
        .with_entities(Purchase.id)\
        .all()
    
    ticketNo = ''
    for ticket in tickets:
        ticketNo += ' ' + str(ticket[0])

    flash (f"Purchase confirmed! Ticket Number/s you have for this event is {ticketNo}", 'success')
    return redirect(url_for('event.details', event_id=event_id))

@event_blueprint.route('/bookings')
@login_required
def bookings():
    bookings = Purchase.query\
        .join(Event, Purchase.event_id == Event.id)\
        .filter(Purchase.user_id == current_user.id)\
        .with_entities(Event.id, Event.description, Event.date, Event.location, Event.name, Purchase.purchase_date, Purchase.id, Event.image)\
        .all()

    if not bookings:
        return render_template('404.html')

    return render_template('bookings.html', bookings=bookings)

@event_blueprint.route('/<int:event_id>/comment', methods=['GET', 'POST'])
@login_required
def comment(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        text = request.form.get('text')
        comment = Comment(text=text, user_id=current_user.id, event_id=event.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added', 'success')
    return redirect(url_for('event_blueprint.details', event_id=event_id))





