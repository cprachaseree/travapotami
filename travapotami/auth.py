from flask import Blueprint, render_template

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/login')
def login():
    # flask automatically enter templates directory when render_template
    return render_template('./auth/login.html', title='Login')