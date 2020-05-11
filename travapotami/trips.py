from flask import Blueprint, render_template, flash, redirect, request, url_for, current_app
from flask_login import current_user
from .forms import TripForm, SearchTripsForm, UpdateTrip, AddHostParticipant
from datetime import date, datetime, timedelta
from .models import db, Trip, User, Group
import pycountry
import sys
from flask_paginate import Pagination, get_page_parameter

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
        t1 = Trip.query.filter(Trip.hosts.contains(current_user)).all()
        t2 = Trip.query.filter(Trip.participants.contains(current_user)).all()
        alltrips = list(set(t1) | set(t2))
        for i in alltrips:
            i.country = pycountry.countries.get(alpha_2=i.destination).name
            i.imagecode = str(i.destination).lower()
        return render_template('./trips/my_trips.html', title='Trips', result=alltrips)
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
    flash(user.username + ' is added to participants!')
    return redirect(url_for('trips_blueprint.requests_manager', tripid=tripid))

@trips_blueprint.route('/trip/<int:tripid>/request_manager/reject/<int:userid>', methods=['GET'])
def participant_reject(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.pending_participants.remove(user)
    db.session.commit()
    flash(user.username + ' is rejected!')
    return redirect(url_for('trips_blueprint.requests_manager', tripid=tripid))

@trips_blueprint.route('/trip/<int:tripid>/remove_participant/<int:userid>', methods=['GET'])
def remove_participant(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.participants.remove(user)
    db.session.commit()
    flash(user.first_name + ' is removed from participants!')
    return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))

@trips_blueprint.route('/trip/<int:tripid>/remove_host/<int:userid>', methods=['GET'])
def remove_host(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.hosts.remove(user)
    db.session.commit()
    flash(user.first_name + ' is removed from hosts!')
    return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))

@trips_blueprint.route('/trip/<int:tripid>/add_host', methods=['GET', 'POST'])
def add_host(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    form = AddHostParticipant()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user != None:
            trip.hosts.append(user)
            db.session.commit()
            return redirect(url_for('trips_blueprint.display_trip', tripid=trip.id))
        else:
            flash("Username does not exist!")
    elif request.method == 'GET':
        return render_template('./trips/add_host_participant.html', title='Add a participant', form=form, trip=trip)

@trips_blueprint.route('/trip/<int:tripid>/add_participant', methods=['GET', 'POST'])
def add_participant(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    form = AddHostParticipant()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user != None:
            trip.participants.append(user)
            db.session.commit()
            return redirect(url_for('trips_blueprint.display_trip', tripid=trip.id))
        else:
            flash("Username does not exist!")
            return render_template('./trips/add_host_participant.html', title='Add a participant', form=form, trip=trip)
    elif request.method == 'GET':
        return render_template('./trips/add_host_participant.html', title='Add a participant', form=form, trip=trip)

@trips_blueprint.route('/trip/<int:tripid>/edit', methods=['GET', 'POST'])
def edit_trip(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    form = UpdateTrip()

    if form.validate_on_submit():
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
        # form.participants.data = trip.participants
        form.description.data = trip.description
        form.datebegin.data = trip.date_from
        form.dateend.data = trip.date_to
        form.max_budget.data = trip.budget_max
        form.triptype.data = trip.trip_type
    return render_template('./trips/edit_trip.html', title='Edit Trip', form=form)


@trips_blueprint.route('/result_trips/<string:destination>/<string:max_budget>/<string:triptype>', methods=['GET'])
def result_trips(destination, max_budget, triptype):
    if max_budget != "None" and triptype != "None":
        result = Trip.query.filter(
            Trip.destination == destination,
            Trip.budget_max <= max_budget,
            Trip.trip_type.like(triptype)
        )
    elif max_budget != "None":
        result = Trip.query.filter(
            Trip.destination == destination,
            Trip.budget_max <= max_budget
        )
    elif triptype != "None":
        result = Trip.query.filter(
            Trip.destination == destination,
            Trip.trip_type.like(triptype)
        )
    else:
        result = Trip.query.filter(
            Trip.destination == destination
        )
    result = result.all()
    for r in result:
        r.country = pycountry.countries.get(alpha_2=r.destination).name
    t1 = Trip.query.filter(Trip.hosts.contains(current_user)).all()
    t2 = Trip.query.filter(
        Trip.participants.contains(current_user)).all()
    mytrips = list(set(t1) | set(t2))
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(result), per_page=3)
    if result:
        flash("Viewing result trips.")
    else:
        flash("Your search returns no query. Please try another one.")
        return redirect(url_for('trips_blueprint.search_trips'))
    return render_template('./trips/result_trips.html', title='Result Trip', result=result, mytrips=mytrips, page=page, pagination=pagination, per_page=3)

@trips_blueprint.route('/search_trip', methods=['GET', 'POST'])
def search_trips():
    if current_user.is_authenticated:
        form = SearchTripsForm()
        if request.method == 'POST':
            if form.max_budget.data != None and not isinstance(float(form.max_budget.data), float) and not isinstance(int(form.max_budget.data), int):
                flash("Max budget should be decimal.")
            else:
                trip_types = list_to_string(form.triptype.data)
                if form.max_budget.data == None:
                    form.max_budget.data = "None"
                if trip_types == None:
                    trip_types = "None"
                max_budget = str(form.max_budget.data)
                return redirect(url_for('trips_blueprint.result_trips', destination=form.destination.data, max_budget=max_budget, triptype=trip_types))
        return render_template('./trips/search_trips.html', title='Search Trip', form=form)
    else:
        flash("Login first please!")
        return redirect(url_for('auth_blueprint.login'))

@trips_blueprint.route('/create_group_trip/<string:group>', methods=['GET', 'POST'])
def create_group_trip(group):
    group = int(''.join(filter(str.isdigit, group)))
    group = Group.query.get(group)
       
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
                    length=timedelta(days=delta.days),
                    trip_type=trip_types
                    )
        db.session.add(trip)

        to_add = []
        for user in group.mates: 
            user = User.query.filter_by(username=user.username).first()
            to_add.append(user)
            flash(f"{user.username} added")
        
        trip.participants = to_add          
        db.session.commit()
        flash("Successfully created trip!")

        group.trips.append(trip)
        db.session.commit()

        return redirect(url_for('trips_blueprint.display_trip', tripid=trip.id))

    return render_template('./trips/create_group_trip.html', title='Create Group Trip', group=group, form=form)

@trips_blueprint.route('/trip/<int:tripid>/finish', methods=['GET', 'POST'])
def finish_trip(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    trip.finished = True
    db.session.commit()
    return redirect(url_for('trips_blueprint.display_trip', tripid=trip.id))

@trips_blueprint.route('/trip/<int:tripid>/delete', methods=['GET', 'POST'])
def delete_trip(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    db.session.delete(trip)
    db.session.commit()
    return redirect(url_for('main_blueprint.home'))
