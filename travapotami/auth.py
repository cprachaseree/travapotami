from flask import Blueprint, render_template, redirect, url_for, request, flash
auth_blueprint = Blueprint('auth_blueprint', __name__)
from .forms import RegistrationForm, LoginForm, ForgotPasswordForm
from . import bcrypt

# Registration page
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
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
