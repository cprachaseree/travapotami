'''
    TRIPS MODULE: Module to process trips related functions.
    PROGRAMMER: Chaichon Wongkham, Laura Torralba
    CALLING SEQUENCE: 
       User on click and on submit to the respective routes
    WHEN: Version 1 written 12-05-2020
    PURPOSE: 
        This module is to process user buttons clicks for certain functionality or user input of submitted forms regarding Trips.
'''
from flask import Blueprint, render_template, flash, redirect, request, url_for, current_app
from flask_login import current_user
from .forms import TripForm, SearchTripsForm, UpdateTrip, AddHostParticipant
from datetime import date, datetime, timedelta
from .models import db, Trip, User, Group
import pycountry
import sys
from flask_paginate import Pagination, get_page_parameter
trips_blueprint = Blueprint('trips_blueprint', __name__)

'''
    LIST_TO_STRING: This function convert a python list of string to one string combining all element with comma-seperated format.
    CALLING SEQUENCE: 
        Used whenever a data that stored in list need to be present to the user. 
        In this app, it is the field trip_types.
    PURPOSE: To aid the printing of information stored as python list.
    DATA STRUCTURE: Python list and string.
    ALGORITHM: For each element, insert it and ', 'in to the output string exccept for the last element.
'''
def list_to_string(input):
    if input is None:
        return None
    st = ""
    for i, trip_type in enumerate(input):
        if i != len(input) - 1:
            st = st + trip_type + ", "
        else:
            st = st + trip_type
'''
    CHOOSE_TRIP: This function simply render page Choose Trip.
    CALLING SEQUENCE: This route is accessed when user click Trip mainmenu.
    PURPOSE: to register URL (route) to the page.
'''
@trips_blueprint.route('/choose_trip')
def choose_trip():
    return render_template('./trips/choose_trip.html', title='Choose Trip')

'''
    CREATE_TRIP: 
        This function recieves user input for a new trip to create it.
        Will redirect to created trip page if successful.
        The operation will not be allowed if the user is not logged in.
    CALLING SEQUENCE: This route is access when user click Create Trip from the Trip main menu.
    PURPOSE: To create a new trip where other users can search for and join.
    DATA STRUCTURE:
        Forms to retrieve user input.
        Database to add the newly created trip to the database.
    ALGORITHM: 
        If user is not authenticated, flash error message and redirect to login page.
        If authenticated, display form.
        After user click submit, use the information from the form to create new trip and redirect to that trip's page.
'''
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
                    length=timedelta(days=delta.days),
                    trip_type=trip_types
                    )
        result = request.form
        db.session.add(trip)
        db.session.commit()
        flash("Successfully created trip!")
        return redirect(url_for('trips_blueprint.display_trip', tripid=trip.id))
    return render_template('./trips/create_trip.html', title='Create Trip', form=form)

'''
    MY_TRIP: This function displayed all trip related to current user (host or participant)
    CALLING SEQUENCE: This route is access when user click My Trip from the Trip main menu.
    PURPOSE: To let all trips related to this user be easily accessible.
    DATA STRUCTURE:
        Forms to retrieve user input.
        Database to query the related trips to the database.
    ALGORITHM: 
        If user is not authenticated, flash error message and redirect to login page.
        If authenticated, search for trips that user is the host.
        THen search for trips that user is the participant.
        Combine the two result and display them.
'''
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

'''
    DISPLAY_TRIP: This function displayed the information of a trip.
    CALLING SEQUENCE: This route is access when user click on a trip from My Trip or Search Trip page.
    PURPOSE: To display all information of a trip.
    DATA STRUCTURE:
        Forms to retrieve user input.
        Database to query the trip to the database.
    ALGORITHM: 
        Search the trip from database according to tripid.
        If current user is host and there are pending participating request, display a notification message.
        Prepare extra information needed by the template.
        Display the page for trip tripid.
'''
@trips_blueprint.route('/trip/<int:tripid>', methods=['GET', 'POST'])
def display_trip(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    if trip.pending_participants and (current_user in trip.hosts):
        flash('Your trip has pending request to join')
    destination = pycountry.countries.get(alpha_2=trip.destination).name
    imagecode = str(trip.destination).lower()
    num_of_hosts = len(trip.hosts)
    return render_template('./trips/display_trip.html', title="Your Trip", trip=trip, destination=destination, imagecode=imagecode, user=current_user, num_of_hosts=num_of_hosts)

'''
    JOIN_TRIP: This function let a user request to join a trip.
    CALLING SEQUENCE: This route is access when user click on Request to Join button on a trip information page.
    PURPOSE: To let user request to join a trip and be approve/reject by hosts.
    DATA STRUCTURE: Database to add the user to request list.
    ALGORITHM: 
        Search the trip from database according to tripid.
        Add currrent user to the trip's pending participant list.
        Flash success message.
        Display the page for trip tripid.
'''
@trips_blueprint.route('/trip/<int:tripid>/join_trip', methods=['GET'])
def join_trip(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    trip.pending_participants.append(current_user)
    db.session.commit()
    flash('Successfully request to join!')
    return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))

'''
    REQUEST_MANAGER: This function let hosts approve/reject join requests.
    CALLING SEQUENCE: This route is access when a host click on Approve/Reject Requests button on a trip information page.
    PURPOSE: To let hosts approve/reject join requests.
    ALGORITHM: 
        Search the trip from database according to tripid and return request manager page for that trip.
'''
@trips_blueprint.route('/trip/<int:tripid>/request_manager', methods=['GET'])
def requests_manager(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    return render_template('./trips/requests_manager.html', title="Manage Requests", trip=trip)

'''
    PARTICIPANT_APPTOVE: This function let hosts approve a join request.
    CALLING SEQUENCE: This route is access when a host click on Approve button for a user on a trip request manager page.
    PURPOSE: To let hosts approve a join request.
    DATA STRUCTURE: Database to add the user to participant list and remove from request list.
    ALGORITHM: 
        Search the trip and user from database according to tripid and userid.
        Add that user to the participant list of the trip.
        Remove that user from the pending participant list.
        Flash success message.
'''
@trips_blueprint.route('/trip/<int:tripid>/request_manager/approve/<int:userid>', methods=['GET'])
def participant_approve(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.pending_participants.remove(user)
    trip.participants.append(user)
    db.session.commit()
    flash(user.username + ' is added to participants!')
    return redirect(url_for('trips_blueprint.requests_manager', tripid=tripid))

'''
    PARTICIPANT_REJECT: This function let hosts reject a join request.
    CALLING SEQUENCE: This route is access when a host click on Reject button for a user on a trip request manager page.
    PURPOSE: To let hosts reject a join request.
    DATA STRUCTURE: Database to remove user from the trip request list.
    ALGORITHM: 
        Search the trip and user from database according to tripid and userid.
        Remove that user from the trip pending participant list.
        Flash success message.
'''
@trips_blueprint.route('/trip/<int:tripid>/request_manager/reject/<int:userid>', methods=['GET'])
def participant_reject(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.pending_participants.remove(user)
    db.session.commit()
    flash(user.username + ' is rejected!')
    return redirect(url_for('trips_blueprint.requests_manager', tripid=tripid))

'''
    REMOVE_PARTICIPANT: This function let hosts remove a participant to the trip.
    CALLING SEQUENCE: This route is access when a host click on Remove button at a user name on a trip information page.
    PURPOSE: To let hosts remove a participant from a trip.
    DATA STRUCTURE: Database to remove user from the trip participant list.
    ALGORITHM: 
        Search the trip and user from database according to tripid and userid.
        Remove that user from the trip participant list.
        Flash success message.
'''
@trips_blueprint.route('/trip/<int:tripid>/remove_participant/<int:userid>', methods=['GET'])
def remove_participant(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.participants.remove(user)
    db.session.commit()
    flash(user.first_name + ' is removed from participants!')
    return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))

'''
    REMOVE_PARTICIPANT: This function let hosts remove a host to the trip.
    CALLING SEQUENCE: This route is access when a host click on Remove button at a host name on a trip information page.
    PURPOSE: To let hosts remove a host from a trip.
    DATA STRUCTURE: Database to remove host from the trip host list.
    ALGORITHM: 
        Search the trip and user from database according to tripid and userid.
        Remove that user from the trip host list.
        Flash success message.
'''
@trips_blueprint.route('/trip/<int:tripid>/remove_host/<int:userid>', methods=['GET'])
def remove_host(tripid, userid):
    trip = Trip.query.filter_by(id=tripid).first()
    user = User.query.filter_by(id=userid).first()
    trip.hosts.remove(user)
    db.session.commit()
    flash(user.first_name + ' is removed from hosts!')
    return redirect(url_for('trips_blueprint.display_trip', tripid=tripid))

'''
    ADD_HOST: This function let hosts add a host to the trip.
    CALLING SEQUENCE: This route is access when a host click on Add button at the host section on a trip information page.
    PURPOSE: To let hosts add a host to the trip.
    DATA STRUCTURE:
        Form to retrieve username input.
        Database to add host to the trip host list.
    ALGORITHM: 
        Search the trip and user from database according to tripid and submitted username.
        If user does not exist, flash error message and return.
        Add that user to the trip host list.
        Flash success message.
'''
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

'''
    ADD_PARTICIPANT: This function let hosts add a participant to the trip.
    CALLING SEQUENCE: This route is access when a host click on Add button at the participant section on a trip information page.
    PURPOSE: To let hosts add a participant to the trip.
    DATA STRUCTURE:
        Form to retrieve username input.
        Database to add participant to the trip participant list.
    ALGORITHM: 
        Search the trip and user from database according to tripid and submitted username.
        If user does not exist, flash error message and return.
        Add that user to the trip participant list.
        Flash success message.
'''
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

'''
    EDIT_TRIP: 
        This function recieves user input for an existing trip to edit it.
        The button to this route is only visible to hosts.
        Will redirect to trip information page if successful.
    CALLING SEQUENCE: This route is access when a host click Edit Trip button from the trip information page.
    PURPOSE: To edit the information of a trip.
    DATA STRUCTURE:
        Forms to retrieve user input.
        Database to add the newly created trip to the database.
    ALGORITHM: 
        Search for the trip from tripid.
        If the form is first access, pre-filled the form with existing data.
        After user click submit, use the information from the form to edit that trip and redirect to that trip's page.
'''
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
        form.description.data = trip.description
        form.datebegin.data = trip.date_from
        form.dateend.data = trip.date_to
        form.max_budget.data = trip.budget_max
        form.triptype.data = trip.trip_type
    return render_template('./trips/edit_trip.html', title='Edit Trip', form=form)

'''
    RESULT_TRIP: 
        This function return the result of searching trip according to criteria from SEARCH_TRIP function.
    CALLING SEQUENCE: This route is access when user click submit on the Search Trip form.
    PURPOSE: To return search result.
    DATA STRUCTURE:
        Database to search the trip according to the criteria given in parameters.
    ALGORITHM: 
        Search the trip from the database according to the given parameter only.
        Prepare extra information needed for the template.
        Flash success message.
        If no trip is found, flash message.
'''
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

'''
    SEARCH_TRIP: 
        This function recieves user input as search criterions to pass on to RESULT_TRIP
    CALLING SEQUENCE: This route is access when a host click Search Trip button from the trip main menu.
    PURPOSE: To let user input search criterions to search trips.
    DATA STRUCTURE:
        Forms to retrieve user input.
    ALGORITHM: 
        Flash error and return if user is not login.
        Do some simple error checking before passing the criterions as parameter to RESULT_TRIP.
'''
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

'''
    CREATE_GROUP_TRIP: 
        This function is the same as CREATE_TRIP but automatically assign all group member to be trip participant and group admin to be trip host.
    CALLING SEQUENCE: This route is access when user click Create Trip from the group main page.
    PURPOSE: To create a new trip specifically for a group.
    DATA STRUCTURE:
        Forms to retrieve user input.
        Database to add the newly created trip to the database.
    ALGORITHM: 
        If user is not authenticated, flash error message and redirect to login page.
        If authenticated, display form.
        After user click submit, use the information from the form to create new trip.
        Add each group member to this trip participant.
        Redirect to that trip's information page.
'''
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

'''
    FINISH_TRIP: This function turn a trip to the finished state.
    CALLING SEQUENCE: This route is access when a host click finish trip in the trip information page.
    PURPOSE: To put trip in the finished state.
    DATA STRUCTURE:
        Database to change trip's attribute
    ALGORITHM:
        Search trip by the tripid then amend finished attribute.
'''
@trips_blueprint.route('/trip/<int:tripid>/finish', methods=['GET', 'POST'])
def finish_trip(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    trip.finished = True
    db.session.commit()
    return redirect(url_for('trips_blueprint.display_trip', tripid=trip.id))

'''
    DELETE: This function delete a trip
    CALLING SEQUENCE: This route is access when a host click delete trip in the trip information page.
    PURPOSE: To delete a trip.
    DATA STRUCTURE:
        Database to change delete a trip record.
    ALGORITHM:
        Search trip by the tripid then delete that record.
'''
@trips_blueprint.route('/trip/<int:tripid>/delete', methods=['GET', 'POST'])
def delete_trip(tripid):
    trip = Trip.query.filter_by(id=tripid).first()
    db.session.delete(trip)
    db.session.commit()
    return redirect(url_for('main_blueprint.home'))
