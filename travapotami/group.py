from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from .models import db, Group, User
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import or_, and_

group_blueprint = Blueprint('group_blueprint', __name__)

@group_blueprint.route('/choose_group')
def choose_group():
    return render_template('./group/choose_group.html', title='Choose Group')

@group_blueprint.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        group_name = request.form['groupname']
        public = request.form.get('accessibility')
        if public:
            public = True
            flash("Public Group")
        else:
            public = False
            flash("Private Group")
        usernames = []
        # get usernames from the form
        for x in request.form:
            if x == "groupname" or not request.form[x] or request.form[x] == 'on':
                continue
            usernames.append(request.form[x])
        #flash(usernames)

        group = Group( group_name = group_name,
                        public = public
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

        flash(f"{group_name} is created with {len(usernames)+1} member(s).")
        return render_template('./group/create_group.html')

    return render_template('./group/create_group.html', title='Create Group')

@group_blueprint.route('/group_info/<string:group>')
def group_info(group):
    group = int(''.join(filter(str.isdigit, group)))
    group = Group.query.get(group)
    return render_template('./group/group_info.html', title='Group Info', group=group)

@group_blueprint.route('/edit_group/<string:group>')
def edit_group(group):
    group = int(''.join(filter(str.isdigit, group)))
    group = Group.query.get(group)
    return render_template('./group/edit_group.html', title='Edit Group', group=group)

@group_blueprint.route('/browse_groups')
def browse_groups():
    result = Group.query.filter_by(public='0').all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(result), per_page=6)
    return render_template('./group/browse_groups.html', title='Browse Groups', result=result, pagination=pagination, page=page, per_page=6)

@group_blueprint.route('/my_groups')
def my_groups():
    result = Group.query.filter(or_(Group.admins.contains(current_user), Group.mates.contains(current_user))).all()
    return render_template('./group/my_groups.html', title='My Groups', result=result)

@group_blueprint.route('/join_group/<string:groupnum>')
def join_group(groupnum):
    groupnum = int(''.join(filter(str.isdigit, groupnum)))
    group = Group.query.get(groupnum)

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
