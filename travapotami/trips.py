from flask import Blueprint, render_template, flash, redirect, request
from .forms import TripForm
trips_blueprint = Blueprint('trips_blueprint', __name__)  # making instance ofblueprint


@trips_blueprint.route('/choose_trip')
def choose_trip():
    return render_template('./trips/choose_trip.html', title='Choose Trip')


@trips_blueprint.route('/create_trip', methods=['GET', 'POST'])
def create_trip():
    form = TripForm()
    if request.method == 'POST':
        result = request.form
        return render_template('./trips/trip.html', title='Created', result=result)
    return render_template('./trips/create_trip.html', title='Create Trip', form=form)


# def edit_trip():
#     return render_template('./trips/edit_trip.html', title='Edit Trip')


# create trip route
# edit trip route
