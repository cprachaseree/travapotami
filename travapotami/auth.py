from base64 import b64encode
from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, UpdateAccountInfo, SearchUsersForm, UpdateImage, GiveRatings, NewPassword
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
auth_blueprint = Blueprint('auth_blueprint', __name__)
from . import bcrypt, login_manager
from .models import db, User, Rating

# Registration page
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # username, email, and passport has to be unique
        has_username = User.query.filter_by(username=form.username.data).first()
        has_email = User.query.filter_by(email=form.email.data).first()
        has_passport = User.query.filter_by(passport_number=form.passport_number.data).first()
        if has_username or has_email or has_passport:
            if has_username:
                flash("Invalid username. Account with this username already exists!")
                form.username.data = None
            if has_email:
                flash("Invalid email. Account with this email already exists.")
                form.email.data = None
            if has_passport:
                flash("Invalid passport number. Account with this passport number already exists.")
                form.passport_number.data = None
        else:
            f = form.photo.data
            f.seek(0)
            data = f.read()
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username        = form.username.data,
                        email           = form.email.data,
                        password        = hashed_password,
                        first_name      = form.first_name.data,
                        last_name       = form.last_name.data,
                        gender          = form.gender.data,
                        passport_number = form.passport_number.data,
                        birthday        = form.birthday.data,
                        photo           = data,
                        is_web_admin    = False
            )

            db.session.add(user)
            db.session.commit()
            flash("Successfully registered. Redirected to login.")
            return redirect(url_for('auth_blueprint.login'))
    if form.errors:
        for i, e in form.errors.items():
            flash(e[0])
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
    if form.errors:
        for i, e in form.errors.items():
            flash(e[0])
    return render_template('./auth/login.html', title='Login', form=form)

# Logout
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out. Redirected to home page.")
    return redirect(url_for('main_blueprint.home'))

# Forget Password
@auth_blueprint.route('/forgetpassword', methods=['GET', 'POST'])
def forgetpassword():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, passport_number=form.passport_number.data).first()
        if user:
            flash("Redirected to change password form.")
            return redirect(url_for('auth_blueprint.new_password', username=user.username))
        else:
            flash("No user exists with given email and passport number.")
    if form.errors:
        for i, e in form.errors.items():
            flash(e[0])
    return render_template('./auth/forgot_password.html', title='Forget Password', form=form)


@auth_blueprint.route('/new_password/<string:username>',  methods=['GET', 'POST'])
def new_password(username):
    form = NewPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        flash("Password resetted! Redirected to login.")
        return redirect(url_for('auth_blueprint.login'))
    return render_template('./auth/new_password.html', title='New Password', form=form)

# Edit user information
@auth_blueprint.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateAccountInfo()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.gender = form.gender.data
            current_user.passport_number = form.passport_number.data
            current_user.birthday = form.birthday.data
            db.session.commit()
            flash('Your account has been updated!')
            return redirect(url_for('auth_blueprint.display_account',
                                    username=current_user.username))
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
    if form.errors:
        for i, e in form.errors.items():
            flash(e[0])
    return render_template('./auth/edit_account.html', title="Update Account",  form=form)


@auth_blueprint.route('/update_photo', methods=['GET', 'POST'])
@login_required
def update_photo():
    form = UpdateImage()
    image = b64encode(current_user.photo).decode("utf-8")
    if form.validate_on_submit():
        f = form.photo.data
        f.seek(0)
        data = f.read()
        current_user.photo = data
        db.session.commit()
        flash("Picture updated.")
        image = b64encode(current_user.photo).decode("utf-8")
        return redirect(url_for('auth_blueprint.display_account', title="View User Profile", username=current_user.username, is_current=True, image=image))
    return render_template('./auth/update_photo.html', title="Update Photo", form=form, image=image)

# display user
@auth_blueprint.route('/user/<string:username>', methods=['GET'])
def display_account(username):
    user = User.query.filter_by(username=username).first()
    is_current = False
    if current_user == user:
        is_current = True
    image = None
    if user.photo:
        image = b64encode(user.photo).decode("utf-8")
    gender = str(user.gender)
    return render_template('./auth/display_account.html', title="View User Profile", user=user, is_current=is_current, image=image, gender=gender)

@auth_blueprint.route('/search_users', methods=['GET', 'POST'])
def search_users():
    form = SearchUsersForm()
    top_friendliness = Rating.query.order_by(Rating.friendliness.desc()).limit(10).all()
    top_cleanliness = Rating.query.order_by(Rating.cleanliness.desc()).limit(10).all()
    top_timeliness = Rating.query.order_by(Rating.timeliness.desc()).limit(10).all()
    top_foodies = Rating.query.order_by(Rating.foodies.desc()).limit(10).all()
    friendly_users = [User.query.filter_by(id=x.user_id).first() for x in top_friendliness]
    clean_users = [User.query.filter_by(id=x.user_id).first() for x in top_cleanliness]
    timely_users = [User.query.filter_by(id=x.user_id).first() for x in top_timeliness]
    food_users = [User.query.filter_by(id=x.user_id).first() for x in top_foodies]

    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user != None:
            return redirect(url_for('auth_blueprint.display_account', username=username))
        else:
            flash("Username does not exist!")
    return render_template('./auth/search_users.html', title="Search Users", form=form, friendly_users=friendly_users, clean_users=clean_users, timely_users=timely_users, food_users=food_users)


@auth_blueprint.route('/rate_user/<string:username>', methods=['GET', 'POST'])
@login_required
def rate_user(username):
    form = GiveRatings()
    if request.method == 'POST':
        is_current = False
        user = User.query.filter_by(username=username).first()
        if user == None:
            flash("Username does not exist!")
            return redirect(url_for('main_blueprint.home'))
        if user == current_user:
            flash("Cannot rate yourself.")
            is_current = True

        number_of_votes = float(user.rating.number_of_votes)
        friendliness = float(user.rating.friendliness)
        cleanliness = float(user.rating.cleanliness)
        timeliness = float(user.rating.timeliness)
        foodies = float(user.rating.foodies)
        friendliness = (friendliness * number_of_votes + float(form.friendliness.data)) / (number_of_votes + 1)
        cleanliness = (cleanliness * number_of_votes + float(form.cleanliness.data)) / (number_of_votes + 1)
        timeliness = (timeliness * number_of_votes + float(form.timeliness.data)) / (number_of_votes + 1)
        foodies = (foodies * number_of_votes + float(form.foodies.data)) / (number_of_votes + 1)

        user.rating.friendliness = friendliness
        user.rating.cleanliness = cleanliness
        user.rating.timeliness = timeliness
        user.rating.foodies = foodies
        user.rating.number_of_votes = number_of_votes + 1
        db.session.commit()

        flash(f"Ratings given to {username}")
        image = user.photo

        return redirect(url_for('auth_blueprint.display_account', title="View User Profile", username=username, is_current=is_current, image=image))

    return render_template('./auth/update_ratings.html', title="Rate User", form=form, username=username)
