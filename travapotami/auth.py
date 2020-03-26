from flask import Blueprint, render_template, redirect, url_for, request, flash
auth_blueprint = Blueprint('auth_blueprint', __name__)
from .forms import RegistrationForm, LoginForm, ForgotPasswordForm

# Registration page
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        flash("Successfully registered. Redirected to login.")
        return redirect(url_for('auth_blueprint.login'))
    return render_template('./auth/register.html', title='Register', form=form)

# Login Page
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        flash("Successfully logged in. Redirected to main.")
        return redirect('/')
    return render_template('./auth/login.html', title='Login', form=form)

# Logout
@auth_blueprint.route('/logout')
def logout():
   
    return render_template('./auth/logout.html', title='Logout')

# Forget Password
@auth_blueprint.route('/forgetpassword',  methods=['GET', 'POST'])
def forgetpassword():
    form = ForgotPasswordForm()
    if request.method == 'POST':
        flash("SUCCESS")
    return render_template('./auth/forgetpassword.html', title='Forget Password', form=form)

# Edit usr information
#@auth_blueprint.route('/edit_user')
def edit_user():
	pass
