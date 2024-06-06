from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from event.models import Event
from event import db
from .forms import LoginForm, RegisterForm
from .models import User, Purchase
from datetime import datetime
from werkzeug.utils import secure_filename
import os

main_blueprint = Blueprint('main', __name__)
event_blueprint = Blueprint('event', __name__, url_prefix='/event')



@main_blueprint.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@main_blueprint.route('/search')
def search():
    if request.args.get('search') and request.args['search'] != "":
        query = "%" + request.args['search'] + "%"
        events = Event.query.filter(Event.description.like(query)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main_blueprint.index'))
    
    
@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.user_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main_blueprint.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main_blueprint.index'))
    return render_template('user.html', title='Sign In', form=form)

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(name=form.user_name.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('main_blueprint.register'))

        user = User(name=form.user_name.data, emailid=form.email_id.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main_blueprint.index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {getattr(form, field).label.text} field - {error}")

    return render_template('register.html', title='Register', form=form)

@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_blueprint.index'))

@event_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        location = request.form.get('location')
        time_str = request.form.get('time')
        date_str = request.form.get('date')
        ticket_price = float(request.form.get('ticket_price'))
        ticket_amount = int(request.form.get('ticket_amount'))
        description = request.form.get('description')
        image_file = request.files.get('image')

        # Handle the image upload
        if image_file:
            filename = secure_filename(image_file.filename)
            image_dir = os.path.join('static', 'images')
            os.makedirs(image_dir, exist_ok=True)  # Ensure directory exists
            image_path = os.path.join(image_dir, filename)
            image_file.save(image_path)
        else:
            image_path = None  # or a default image path

        try:
            time_obj = datetime.strptime(time_str, '%H:%M').time()
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid time or date format', 'error')
            return redirect(url_for('event_blueprint.create'))

        new_event = Event(
            location=location,
            time=time_obj,
            date=date_obj,
            ticket_price=ticket_price,
            ticket_amount=ticket_amount,
            description=description,
            image=image_path  # Set the image field
        )
        db.session.add(new_event)
        db.session.commit()

        flash('Event successfully created!', 'success')
        return redirect(url_for('main_blueprint.index'))

    return render_template('create_event.html')

@event_blueprint.route('/details/<int:event_id>', methods=['GET'])
def details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_details.html', event=event)

# Ensure other routes also use event_blueprint for url_for

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
def confirm_purchase(event_id): #process purchase of tickets
    event = Event.query.get_or_404(event_id)
    ticket_quantity = int(request.form.get('ticket_quantity'))
    if ticket_quantity > event.ticket_amount:
        flash('Not enough tickets available.', 'error')
        return redirect(url_for('event_blueprint.details', event_id=event_id))

    event.ticket_amount = event.ticket_amount - ticket_quantity  # Decrease the available tickets

    for _ in range(ticket_quantity): #create new entries for each ticket purchased 
        purchase_ticket = Purchase(user_id=current_user.id, event_id=event.id)
        db.session.add(purchase_ticket)
    db.session.add(event)
    db.session.commit()

    flash('Purchase confirmed!', 'success')
    return redirect(url_for('event_blueprint.details', event_id=event_id))
from event import eventbp
