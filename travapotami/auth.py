from flask import Blueprint, render_template

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/login')
def login():
    # flask automatically enter templates directory when render_template
    return render_template('./auth/login.html', title='Login')

@auth_blueprint.route('/register')
def register():
    # flask automatically enter templates directory when render_template
    return render_template('./auth/register.html', title='Register')

@auth_blueprint.route('/logout')
def logout():
    # flask automatically enter templates directory when render_template
    return render_template('./auth/logout.html', title='Login')