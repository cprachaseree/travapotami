from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import current_user
from .forms import TripForm, SearchTripsForm
from datetime import date, datetime, timedelta
from .models import db, Trip
trips_blueprint = Blueprint('trips_blueprint', __name__)  # making instance ofblueprint


@trips_blueprint.route('/choose_trip')
def choose_trip():
    return render_template('./trips/choose_trip.html', title='Choose Trip')

@trips_blueprint.route('/create_trip', methods=['GET', 'POST'])
def create_trip():
    if not current_user.is_authenticated:
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
        trip = Trip(hosts=[current_user],
                    destination=form.destination.data,
                    budget_max=form.max_budget.data,
                    date_from=form.datebegin.data,
                    date_to=form.dateend.data,
                    description=form.description.data,
                    # date_from=datetime.combine(form.datebegin.data, time()),
                    # date_to=datetime.combine(form.dateend.data, time()),
                    length=timedelta(days=delta.days),
                    trip_type=form.triptype.data
                    )
        result = request.form
        db.session.add(trip)
        db.session.commit()
        flash("Successfully created trip!")
        return render_template('./trips/trip.html', title='Created', result=result)
    return render_template('./trips/create_trip.html', title='Create Trip', form=form)


@trips_blueprint.route('/my_trips', methods=['GET', 'POST'])
def my_trips():

    return render_template('./trips/my_trips.html', title='Trips', result=result)

# def edit_trip():
#     return render_template('./trips/edit_trip.html', title='Edit Trip')

@trips_blueprint.route('/search_trip', methods=['GET', 'POST'])
def search_trips():
    form = SearchTripsForm()
    if form.validate_on_submit():
        db.session
    
    return render_template('./trips/search_trips.html', title='Search Trip', form=form)
        
