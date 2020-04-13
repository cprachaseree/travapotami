from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, UpdateAccountInfo
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
auth_blueprint = Blueprint('auth_blueprint', __name__)
from . import bcrypt, login_manager
from .models import db, User

# Registration page
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username        = form.username.data,
                    email           = form.username.data,
                    password        = hashed_password,
                    first_name      = form.first_name.data,
                    last_name       = form.last_name.data,
                    gender          = form.gender.data,
                    passport_number = form.passport_number.data,
                    birthday        = form.birthday.data
        )
        db.session.add(user)
        db.session.commit()
        flash("Successfully registered. Redirected to login.")
        return redirect(url_for('auth_blueprint.login'))
    return render_template('./auth/register.html', title='Register', form=form)

# Login Page
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in. Redirected to home page.")
            return redirect(url_for('main_blueprint.home'))
        else:
            flash("Incorrect username or password. Please try again.")
    return render_template('./auth/login.html', title='Login', form=form)

# Logout
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out. Redirected to home page.")
    return redirect(url_for('main_blueprint.home'))

# Forget Password
@auth_blueprint.route('/forgetpassword',  methods=['GET', 'POST'])
def forgetpassword():
    form = ForgotPasswordForm()
    if request.method == 'POST':
        flash("SUCCESS")
    return render_template('./auth/forgetpassword.html', title='Forget Password', form=form)

# Edit usr information
@auth_blueprint.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateAccountInfo()
    if form.validate_on_submit():
        if bcrypt.generate_password_hash(current_user.password, form.password.data):
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.gender = form.gender.data
            current_user.passport_number = form.passport_number.data
            current_user.birthday = form.birthday.data
            db.session.commit()
            flash('Your account has been updated!')
            return redirect(url_for('main_blueprint.home'))
        else:
            flash('Incorrect password. Please try again or cancel.')
            return redirect(url_for('auth_blueprint.edit_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.gender.data = current_user.gender
        form.passport_number.data = current_user.passport_number
        form.birthday.data = current_user.birthday
    return render_template('./auth/edit_account.html', title="Update Account",  form=form)
