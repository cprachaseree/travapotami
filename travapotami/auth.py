from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
auth_blueprint = Blueprint('auth_blueprint', __name__)
from .forms import RegistrationForm, LoginForm, ForgotPasswordForm
from . import bcrypt

# Registration page
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    #if current_user.is_authenticated:
        #return redirect(url_for('main.home'))
    form = RegistrationForm()
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        '''
        user = User(username=form.username.data,
                    email=form.username.data
                    password=hashed_password,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    gender=form.gender.data,
                    passport_no=form.passport_no.data,
                    date_of_birth=form.data_of_birth.data
        )
        !!!! HAS NOT IMPORT db YET !!!!!
        db.session.add(user)
        db.session.commit()
        '''
        flash(f"Hashed password is {hashed_password}")
        flash("Successfully registered. Redirected to login.")
        return redirect(url_for('auth_blueprint.login'))
    return render_template('./auth/register.html', title='Register', form=form)

# Login Page
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
        #return redirect(url_for('main.home'))
    form = LoginForm()
    if request.method == 'POST':
        # for testing
        # validate user
        #if validate:
            #user = "USER"
            #login_user(user)
            #flash("Successfully logged in. Redirected to main.")
        return redirect(url_for('main.home'))
        #else:
            # flash("Unsuccessful log in. Please try again.")
    return render_template('./auth/login.html', title='Login', form=form)

# Logout
@auth_blueprint.route('/logout')
@login_required
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
#@login_required
def edit_user():
	pass
