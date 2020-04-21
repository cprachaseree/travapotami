from flask import Blueprint, render_template, flash, redirect, request
from flask_login import current_user
from .forms import TripForm
from datetime import date, datetime, timedelta
from .models import db, Trip
trips_blueprint = Blueprint('trips_blueprint', __name__)  # making instance ofblueprint


@trips_blueprint.route('/choose_trip')
def choose_trip():
    return render_template('./trips/choose_trip.html', title='Choose Trip')


@trips_blueprint.route('/create_trip', methods=['GET', 'POST'])
def create_trip():
    form = TripForm()
    start_month = str(form.datebegin.data)[5:7]
    start_day = str(form.datebegin.data)[8:]
    start_year = str(form.datebegin.data)[:4]
    end_month = str(form.dateend.data)[5:7]
    end_day = str(form.dateend.data)[8:]
    end_year = str(form.dateend.data)[:4]
    d0 = date(int(start_year), int(start_month), int(start_day))
    d1 = date(int(end_year), int(end_month), int(end_day))
    delta = d1 - d0
  #  print(delta.days)

    if request.method == 'POST':
        trip = Trip(destination=form.destination.data,
                    budget_min=form.min_budget.data,
                    budget_max=form.max_budget.data,
                    date_from=form.datebegin.data,
                    date_to=form.dateend.data,
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


# def edit_trip():
#     return render_template('./trips/edit_trip.html', title='Edit Trip')


# create trip route
# edit trip route
