from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import current_user
from .forms import TripForm, SearchTripsForm, UpdateTrip
from datetime import date, datetime, timedelta
from .models import db, Trip
import pycountry
trips_blueprint = Blueprint('trips_blueprint', __name__)  # making instance ofblueprint


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
        trip_types = ""
        for i, trip_type in enumerate(form.triptype.data):
            if i != len(form.triptype.data) - 1:
                trip_types = trip_types + trip_type + ", "
            else:
                trip_types = trip_types + trip_type
        
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
        return render_template('./trips/trip.html', title='Created', result=result)
    return render_template('./trips/create_trip.html', title='Create Trip', form=form)


@trips_blueprint.route('/my_trips', methods=['GET', 'POST'])
def my_trips():
    if current_user.is_authenticated:
        alltrips = Trip.query.filter(Trip.hosts.contains(current_user)).all()
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
    new = {}
    new['tripid'] = trip.id
    if trip.hosts:
        hosts = []
        hostusername = []
        for x in trip.hosts:
            hosts.append(x.first_name + " " + x.last_name)  # i.hosts is a list
            hostusername.append(x.username)
        new['hosts'] = hosts
        new['hostusername'] = hostusername
    country = pycountry.countries.get(alpha_2=trip.destination)  # append as country.name
    new['destination'] = country.name
    if trip.participants:
        new['participants'] = trip.participants
    new['budget_max'] = trip.budget_max
    new['date_from'] = trip.date_from
    new['date_to'] = trip.date_to
    new['length'] = trip.length  # in days
    new['trip_type'] = trip.trip_type
    new['imagecode'] = str(trip.destination).lower()
    new['user'] = current_user.username
    return render_template('./trips/display_trip.html', title="Your trip", result=new)


@trips_blueprint.route('/join_trip', methods=['GET', 'POST'])
def join_trips():
    return render_template('./trips/choose_trip.html', title='Choose Trip')


@trips_blueprint.route('/edit_trip/<int:tripid>', methods=['GET', 'POST'])
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
        form.description.data = trip.description
        form.datebegin.data = trip.date_from
        form.dateend.data = trip.date_to
        form.max_budget.data = trip.budget_max
        form.destination.data = trip.trip_type
    return render_template('./trips/edit_trip.html', title='Edit Trip', form=form)


@trips_blueprint.route('/search_trip', methods=['GET', 'POST'])
def search_trips():
    form = SearchTripsForm()
    if form.validate_on_submit():
        db.session

    return render_template('./trips/search_trips.html', title='Search Trip', form=form)
