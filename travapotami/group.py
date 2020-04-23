from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from .models import db, Group, User, Trip
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import or_, and_
import pycountry

group_blueprint = Blueprint('group_blueprint', __name__)

@group_blueprint.route('/choose_group')
def choose_group():
    return render_template('./group/choose_group.html', title='Choose Group')

@group_blueprint.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if current_user.is_authenticated:
        if request.method == 'POST':
            group_name = request.form['groupname']
            public = request.form.get('accessibility')
            description = request.form['group-description']
            icon = request.form['icon']
            flash(icon)

            if public:
                public = True
                flash("Public Group")
            else:
                public = False
                flash("Private Group")
            usernames = []
            # get usernames from the form
            for x in request.form:
                if x == "groupname" or x == "group-description" or not request.form[x] or request.form[x] == 'on':
                    continue
                usernames.append(request.form[x])
            #flash(usernames)

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

            flash(f"{group_name} is created with {len(to_add)+1} member(s).")
            return render_template('./group/create_group.html')

        return render_template('./group/create_group.html', title='Create Group')

    else:
        flash("Login first please!")
        return redirect(url_for('auth_blueprint.login')) 

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

@group_blueprint.route('/browse_groups', methods=['GET', 'POST'])
def browse_groups():
    if request.method == 'POST':
        flash(request.form['search'])
        result = Group.query.filter_by(group_name=request.form['search']).all()
        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, total=len(result), per_page=6)       
        return render_template('./group/browse_groups.html', title='Browse Groups', result=result, pagination=pagination, page=page, per_page=6)
    
    result = Group.query.filter_by(public='1').all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(result), per_page=6)
    return render_template('./group/browse_groups.html', title='Browse Groups', result=result, pagination=pagination, page=page, per_page=6)


@group_blueprint.route('/my_groups')
def my_groups():
    if current_user.is_authenticated:
        result = Group.query.filter(or_(Group.admins.contains(current_user), Group.mates.contains(current_user))).all()
        return render_template('./group/my_groups.html', title='My Groups', result=result)
    else:
        flash("Login first please!")
        return redirect(url_for('auth_blueprint.login'))

@group_blueprint.route('/join_group/<string:groupnum>')
def join_group(groupnum):
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

@group_blueprint.route('/leave_group/<string:group>')
def leave_group(group):
    group = int(''.join(filter(str.isdigit, group)))
    flash(group)
    group = Group.query.get(group)
    group.mates.remove(current_user)
    db.session.commit()
    flash("Successfully Leave Group")
    return redirect(url_for('group_blueprint.my_groups'))

@group_blueprint.route('/delete_group/<string:group>')
def delete_group(group):
    flash("Delete Group")
    group = int(''.join(filter(str.isdigit, group)))
    group = Group.query.get(group)
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('group_blueprint.my_groups'))
