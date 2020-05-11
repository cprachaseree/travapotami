'''
    GROUP MODULE: Module to prcess group related functions
    PROGRAMMER: Pareeyaporn Prachaseree
    CALLING SEQUENCE: When user or admin select the respective routes
    WHEN: Version 1 written 11-05-2020
    PURPOSE: This module aims to redirects users to the correct forms and buttons after user clicks
'''
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from .models import db, Group, User, Trip
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import or_, and_
import pycountry

group_blueprint = Blueprint('group_blueprint', __name__)

'''
    CHOOSE_GROUP: This page serves as a main page for groups. It asks the user their next step.
    CALLING SEQUENCE: This route is accessed when the user clicks "Groups" in the navigation bar. 
    PURPOSE: To be used when the user wants to create an account to use the web application.
    DATA STRUCTURES: None
    ALGORITHM: User selects their next choice, and the url directs them to the corresponding page. 
'''
@group_blueprint.route('/choose_group')
def choose_group():
    return render_template('./group/choose_group.html', title='Choose Group')

'''
    CREATE_GROUP: This function receives user input to form a new group.
                  Will return a redirect to login if users have not yet login.
    CALLING SEQUENCE: This route is accessed when user clicks "Create a new group" under group main page.
    PURPOSE: For users to create a new group, the group creater is the group admin.
    DATA STRUCTURES: Forms - to accept user input
                     Database - to insert new group, to query existing usernames
    ALGORITHM:  Ask for group name, icon, description, public/private, and groupmates by username
                Flashes when group successfully created, and who is added into the group
'''
@group_blueprint.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if current_user.is_authenticated:
        if request.method == 'POST':
            group_name = request.form['groupname']
            public = request.form.get('accessibility')
            description = request.form['group-description']
            icon = request.form['icon']

            if public:
                public = True
            else:
                public = False
            usernames = []
            # get usernames from the form
            for x in request.form:
                if x == "groupname" or x == "group-description" or x == 'icon' or not request.form[x] or request.form[x] == 'on':
                    continue
                usernames.append(request.form[x])

            group = Group( group_name = group_name,
                            public = public,
                            description = description,
                            icon = icon
            )
            db.session.add(group)
            db.session.commit()
            group.admins = [current_user]
            db.session.commit()

            to_add = []
            for username in usernames: 
                user = User.query.filter_by(username=username).first()
                if user != None:
                    to_add.append(user)
                    flash(f"{username} added")
                else:
                    flash(f"{username} does not exist!")
            group.mates = to_add
            db.session.commit()
            flash ("New group is created.")
            return redirect(url_for('group_blueprint.my_groups'))

        return render_template('./group/create_group.html', title='Create Group')

    else:
        flash("Login first please!")
        return redirect(url_for('auth_blueprint.login')) 

'''
    GROUP_INFO: This function retrieves group information, both group details and group trips.
                The page is slightly different depending on whether you are the admin of the group,
                a group mate, or not both.
    CALLING SEQUENCE: This route is accessed when user clicks to view more details of each group.
                There are several buttons that can lead to this page. 
                Ex. when viewing my groups or browsing groups
    DATA STRUCTURES: Database - to query existing groups
    ALGORITHM: Get the group_id of the group the user is interested in viewing, query the group_id 
            in the group database. Check to see whether the user is a group admin, group mate, 
            or neither of the two for the group he/she is trying the view. Check whether there are any 
            group trips tied to this group_id.
'''
@group_blueprint.route('/group_info/<string:group>')
def group_info(group):
    group = int(''.join(filter(str.isdigit, group)))
    searchgroup = Group.query.filter_by(id=group).first()
    group = Group.query.get(group)

    if current_user == searchgroup.admins[0]:
        is_admin = True
    else:
        is_admin = False
    
    if current_user in searchgroup.mates:
        is_mate = True
    else:
        is_mate = False
    
    for i in group.trips:
        i.country = pycountry.countries.get(alpha_2=i.destination).name
        i.imagecode = str(i.destination).lower()

    return render_template('./group/group_info.html', title='Group Info', group=group, is_admin=is_admin, is_mate=is_mate)

'''
    EDIT_GROUP: This function allows the admin the edit group information.
    CALLING SEQUENCE: This route is accessed when the group admin clicks "edit group" in group info page
    DATA STRUCTURES: Database - to query and update existing groups
    ALGORITHM: Query the group_id from the database, and get group info. Update the new info.
               Flash if there is any error in submission. Ex. add users who are already in group.
'''
@group_blueprint.route('/edit_group/<string:group>',  methods=['GET', 'POST'])
def edit_group(group):
    groupnum = int(''.join(filter(str.isdigit, group)))
    group = Group.query.get(groupnum)

    if request.method == 'POST':
        group_name = request.form['groupname']
        public = request.form.get('accessibility')
        description = request.form['group-description']
        icon = request.form['icon']

        if public:
            public = True
        else:
            public = False
        usernames = []

        for x in request.form:
            if x == "groupname" or x == "group-description" or not request.form[x] or request.form[x] == 'on':
                continue
            usernames.append(request.form[x])
        
        group.group_name = group_name
        group.public = public
        group.description = description
        group.icon = icon

        to_add = []
        group_search = Group.query.filter_by(id=groupnum).first()
        for username in usernames: 
            user_search = User.query.filter_by(username=username).first()
            if user_search != None:
                if not user_search in group_search.mates or not user_search in group_search.admins:
                    to_add.append(user_search)
                    flash(f"{user_search.username} added to group")
                else:
                    flash(f"{user_search.username} already in group!")
        group.mates = to_add
        db.session.commit()
        flash("Your group is edited")
        return redirect(url_for('group_blueprint.my_groups'))
    return render_template('./group/edit_group.html', title='Edit Group', group=group)

'''
    BROWSE_GROUPS: This function displays all public groups in the database
    CALLING SEQUENCE: This route is accessed when user clicks to "Browse Groups" in the group main page.
    DATA STRUCTURES: Database - to query existing groups
    ALGORITHM: Searches for all the public groups in the database. Uses pagination function to 
                divide the search result into different pages, with 6 per page.
'''
@group_blueprint.route('/browse_groups', methods=['GET', 'POST'])
def browse_groups():
    if request.method == 'POST':
        return redirect(url_for('group_blueprint.browse_search_groups', searchgroup=request.form['search']))
    result = Group.query.filter_by(public='1').all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(result), per_page=6)
    return render_template('./group/browse_groups.html', title='Browse Groups', result=result, pagination=pagination, page=page, per_page=6)

'''
    BROWSE_SEARCH_GROUPS: This function displays all user input group name in the database
    CALLING SEQUENCE: This route is accessed when user searches in "Browse Groups".
    DATA STRUCTURES: Database - to query existing groups
    ALGORITHM: Searches for all the corresponding groups the in the database. Uses pagination function to 
                divide the search result into different pages, with 6 per page.
'''
@group_blueprint.route('/browse_search_groups/<string:searchgroup>')
def browse_search_groups(searchgroup):
    result = Group.query.filter_by(group_name=searchgroup).all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(result), per_page=6)       
    return render_template('./group/browse_search_groups.html', title='Browse Groups', result=result, pagination=pagination, page=page, per_page=6)

'''
    MY_GROUPS: This function displays all the groups the user is in
    CALLING SEQUENCE: This route is accessed when user clicks in "My Groups".
    DATA STRUCTURES: Database - to query existing groups
    ALGORITHM: Searches for all the user's group the database, including those being the admin and groupmates.
                If user is not logged in redirect to log in page.
'''
@group_blueprint.route('/my_groups')
def my_groups():
    if current_user.is_authenticated:
        result = Group.query.filter(or_(Group.admins.contains(current_user), Group.mates.contains(current_user))).all()
        return render_template('./group/my_groups.html', title='My Groups', result=result)
    else:
        flash("Login first please!")
        return redirect(url_for('auth_blueprint.login'))

'''
    JOIN_GROUP: This function adds user into a new group.
    CALLING SEQUENCE: This route is accessed when pressed "Join Group". There are 2 paths, user can press "Join"
                    in group info page, or when browsing through "Browse Group" page. 
    DATA STRUCTURES: Database - to query and update existing groups
    ALGORITHM: Get group id. If user is admin or groupmate, flash error. Else add user add as new groupmate.
                Redirects back to browse group page.
                If user is not logged in redirect to log in page.
'''
@group_blueprint.route('/join_group/<string:groupnum>')
def join_group(groupnum):
    if current_user.is_authenticated:
        groupnum = int(''.join(filter(str.isdigit, groupnum)))
        group = Group.query.filter_by(id=groupnum).first()
        if current_user == group.admins[0]:
            flash("You are the admin of this group!")
        elif current_user in group.mates:
            flash("You are already one of the group mates.")
        else:
            group.mates = [current_user]
            db.session.commit()
            flash(f"Successfully Joined {group.group_name}")
        return redirect(url_for('group_blueprint.browse_groups'))
    else:
        flash("Login first please!")
        return redirect(url_for('auth_blueprint.login'))

'''
    LEAVE_GROUP: This function deletes user from the group.
    CALLING SEQUENCE: This route is accessed when user clicks "Leave Group" in group info page.
    DATA STRUCTURES: Database - to query and update existing groups
    ALGORITHM: Get group id. Remove the current user from group. Flashes success message to user.
'''
@group_blueprint.route('/leave_group/<string:group>')
def leave_group(group):
    group = int(''.join(filter(str.isdigit, group)))
    group = Group.query.get(group)
    group.mates.remove(current_user)
    db.session.commit()
    flash("Successfully Leave Group")
    return redirect(url_for('group_blueprint.my_groups'))

'''
    DELETE_GROUP: This function deletes group from database
    CALLING SEQUENCE: This route is accessed when group admin clicks "Delete Group" in group info page.
    DATA STRUCTURES: Database - to query and update existing groups
    ALGORITHM: Get group id. Remove group from database. If deleted, flash message to user.
'''
@group_blueprint.route('/delete_group/<string:group>')
def delete_group(group):
    flash("Deleted Group")
    group = int(''.join(filter(str.isdigit, group)))
    group = Group.query.get(group)
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('group_blueprint.my_groups'))