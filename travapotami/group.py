from flask import Blueprint, render_template, request, flash

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
            if x == "groupname" or not request.form[x]:
                continue
            usernames.append(request.form[x])
        flash(f"{group_name} is created with {len(usernames)+1} member(s).")
        # TODO find userid of all users with the given username and add to the group
        return render_template('./group/create_group.html')
    return render_template('./group/create_group.html', title='Create Group')

@group_blueprint.route('/edit_group')
def edit_group():
    return render_template('./group/edit_group.html', title='Edit Group')

@group_blueprint.route('/browse_groups')
def browse_groups():
    return render_template('./group/browse_groups.html', title='Browse Groups')

@group_blueprint.route('/my_groups')
def my_groups():
    return render_template('./group/my_groups.html', title='My Groups')