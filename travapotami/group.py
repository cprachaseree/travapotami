from flask import Blueprint, render_template

group_blueprint = Blueprint('group_blueprint', __name__)

@group_blueprint.route('/create_group')
def create_group():
    return render_template('./group/create_group.html', title='Create Group')
