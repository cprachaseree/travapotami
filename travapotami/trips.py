from flask import Blueprint, render_template, flash, redirect, request, url_for, current_app
from flask_login import current_user
from .forms import TripForm, SearchTripsForm, UpdateTrip
from datetime import date, datetime, timedelta
from .models import db, Trip, User
import pycountry
import sys
trips_blueprint = Blueprint('trips_blueprint', __name__)  # making instance ofblueprint

def list_to_string(input):
    if input is None:
        return None
    st = ""
    for i, trip_type in enumerate(input):
        if i != len(input) - 1:
            st = st + trip_type + ", "
        else:
            st = st + trip_type

@trips_blueprint.route('/choose_trip')
def choose_trip():
    return render_template('./trips/choose_trip.html', title='Choose Trip')


@trips_blueprint.route('/create_trip', methods=['GET', 'POST'])
def create_trip():
    if not current_user.is_authenticated:
        flash("Login first please!")
        return redirect(url_for('auth_blueprint.login'))

    form = TripForm()
    if form.validate_on_submit():
        start_month = str(form.datebegin.data)[5:7]
        start_day = str(form.datebegin.data)[8:]
        start_year = str(form.datebegin.data)[:4]
        end_month = str(form.dateend.data)[5:7]
        end_day = str(form.dateend.data)[8:]
        end_year = str(form.dateend.data)[:4]
        d0 = date(int(start_year), int(start_month), int(start_day))
        d1 = date(int(end_year), int(end_month), int(end_day))
        delta = d1 - d0
        trip_types = list_to_string(form.triptype.data)
        
        trip = Trip(hosts=[current_user],
                    destination=form.destination.data,
                    budget_max=form.max_budget.data,
                    date_from=form.datebegin.data,
                    date_to=form.dateend.data,
                    description=form.description.data,
                    # date_from=datetime.combine(form.datebegin.data, time()),
                    # date_to=datetime.combine(form.dateend.data, time()),
                    length=timedelta(days=delta.days),
                    trip_type=trip_types
                    )
        result = request.form
        db.session.add(trip)
        db.session.commit()
        flash("Successfully created trip!")
        return redirect(url_for('trips_blueprint.display_trip', tripid=trip.id))
    return render_template('./trips/create_trip.html', title='Create Trip', form=form)


@trips_blueprint.route('/my_trips', methods=['GET', 'POST'])
def my_trips():
    if current_user.is_authenticated:
        alltrips = Trip.query.filter(Trip.hosts.contains(current_user)).all()
        list2 = Trip.query.filter(Trip.participants.contains(current_user)).all()
        for x in list2:
            alltrips.append(x)
        trips = []
        for i in alltrips:
            new = {}
            new['tripid'] = i.id
            if i.hosts:
                hosts = []
                for x in i.hosts:
                    hosts.append(x.first_name + " " + x.last_name)  # i.hosts is a list
                new['hosts'] = hosts
            country = pycountry.countries.get(alpha_2=i.destination)  # append as country.name
            new['destination'] = country.name
            if i.participants:
                new['participants'] = i.participants
            new['budget_max'] = i.budget_max
            new['date_from'] = i.date_from
            new['date_to'] = i.date_to
            new['length'] = i.length  # in days
            new['trip_type'] = i.trip_type
            new['imagecode'] = str(i.destination).lower()
            trips.append(new)
        return render_template('./trips/my_trips.html', title='Trips', result=trips)
    else:
        flash("Login first please!")
        return redirect(url_for('auth_blueprint.login'))


@trips_blueprint.route('/trip/<int:tripid>', methods=['GET', 'POST'])
def display_trip(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    if trip.pending_participants and (current_user in trip.hosts):
        flash('Your trip has pending request to join')
    destination = pycountry.countries.get(alpha_2=trip.destination).name
    imagecode = str(trip.destination).lower()
    num_of_hosts = len(trip.hosts)
    return render_template('./trips/display_trip.html', title="Your Trip", trip=trip, destination=destination, imagecode=imagecode, user=current_user, num_of_hosts=num_of_hosts)

@trips_blueprint.route('/trip/<int:tripid>/join_trip', methods=['GET'])
def join_trip(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    trip.pending_participants.append(current_user)
    db.session.commit()
    flash('Successfully request to join!')
    return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))

@trips_blueprint.route('/trip/<int:tripid>/request_manager', methods=['GET'])
def requests_manager(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    return render_template('./trips/requests_manager.html', title="Manage Requests", trip=trip)

@trips_blueprint.route('/trip/<int:tripid>/request_manager/approve/<int:userid>', methods=['GET'])
def participant_approve(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.pending_participants.remove(user)
    trip.participants.append(user)
    db.session.commit()
    flash(user.name + 'is added to participants!')
    return redirect(url_for('trips_blueprint.requests_manager', tripid=tripid))

@trips_blueprint.route('/trip/<int:tripid>/request_manager/reject/<int:userid>', methods=['GET'])
def participant_reject(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.pending_participants.remove(user)
    db.session.commit()
    flash(user.name + 'is rejected!')
    return redirect(url_for('trips_blueprint.requests_manager', tripid=tripid))

@trips_blueprint.route('/trip/<int:tripid>/remove_participant/<int:userid>', methods=['GET'])
def remove_participant(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.participants.remove(user)
    db.session.commit()
    flash(user.first_name + 'is removed from participants!')
    return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))

@trips_blueprint.route('/trip/<int:tripid>/remove_host/<int:userid>', methods=['GET'])
def remove_host(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.hosts.remove(user)
    db.session.commit()
    flash(user.first_name + 'is removed from hosts!')
    return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))

# @trips_blueprint.route('/trip/<int:tripid>/add_host/<int:userid>', methods=['GET'])
# def add_host(tripid, userid):
#     trip = Trip.query.filter_by(id=tripid).first()
#     user = User.query.filter_by(id=userid).first()
#     trip.hosts.append(user)
#     db.session.commit()
#     flash(user.first_name + 'is added to hosts!')
#     return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))

# @trips_blueprint.route('/trip/<int:tripid>/add_participant/<int:userid>', methods=['GET'])
# def add_participants(tripid, userid):
#     trip = Trip.query.filter_by(id=tripid).first()
#     user = User.query.filter_by(id=userid).first()
#     trip.participants.append(user)
#     db.session.commit()
#     flash(user.first_name + 'is added to participants!')
#     return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))

@trips_blueprint.route('/trip/<int:tripid>/edit', methods=['GET', 'POST'])
def edit_trip(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    form = UpdateTrip()

    if form.validate_on_submit():
        if form.participants:
            usernames = str(form.participants.data).split(',')
            participants = []
            for x in usernames:
                user1 = User.query.filter_by(username=x).first()
                if user1:
                    participants.append(user1)
                    flash(str(x) + 'added to the trip')
                else:
                    flash(str(x) + 'does not exist')
            trip.participants = participants
        if form.participantsremoved:
            usernames = str(form.participants.data).split(',')
            for x in usernames:
                user1 = User.query.filter_by(username=x).first()
                if user1:
                    participanttrips = Trip.query.filter(Trip.participants.contains(user1)).all()  # list of trips
                    hostingtrips = Trip.query.filter_by(Trip.hosts.contains(user1)).all()  # list of trips
                    for y in hostingtrips:
                        y.hosts.remove(user1)
                    for y in participanttrips:
                        y.participants.remove(user1)
        trip.destination = form.destination.data
        trip.description = form.description.data
        trip.date_from = form.datebegin.data
        trip.date_to = form.dateend.data
        trip.budget_max = form.max_budget.data
        trip.trip_type = form.triptype.data
        db.session.commit()
        flash('Your trip has been updated!')
        return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))
    elif request.method == 'GET':
        form.destination.data = trip.destination
        form.participants.data = trip.participants
        form.description.data = trip.description
        form.datebegin.data = trip.date_from
        form.dateend.data = trip.date_to
        form.max_budget.data = trip.budget_max
        form.triptype.data = trip.trip_type
    return render_template('./trips/edit_trip.html', title='Edit Trip', form=form)


@trips_blueprint.route('/search_trip', methods=['GET', 'POST'])
def search_trips():
    form = SearchTripsForm()
    result = None
    trip_types = list_to_string(form.triptype.data)

    if request.method == 'POST':
        if form.max_budget.data != None and not isinstance(float(form.max_budget.data), float) and not isinstance(int(form.max_budget.data), int):
            flash("Max budget should be decimal.")
        else:
            if form.max_budget.data and form.triptype.data:
                result = Trip.query.filter(
                    Trip.destination == form.destination.data,
                    Trip.budget_max <= form.max_budget.data,
                    Trip.trip_type.like(trip_types)
                )
            elif form.max_budget.data:
                result = Trip.query.filter(
                    Trip.destination == form.destination.data,
                    Trip.budget_max <= form.max_budget.data
                )
            elif form.triptype.data:
                result = Trip.query.filter(
                    Trip.destination == form.destination.data,
                    Trip.trip_type.like(trip_types)
                )
            else:
                result = Trip.query.filter(
                    Trip.destination == form.destination.data
                )
            if result:
                result = result.all()
                # view the trips
                flash("Viewing result trips.")
                pass
            else:
                flash("Your search returns no query. Please try another one.")
    if form.errors:
        for i, e in form.errors.items():
            flash(f"{i}: {e}")
    return render_template('./trips/search_trips.html', title='Search Trip', form=form)

