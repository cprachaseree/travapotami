'''
    MODELS MODULE: Module to define all database (class) definition
    PROGRAMMER: Chaichon Wongkham
    CALLING SEQUENCE: 
        The class definition would be used by SQLALchemy db object to initialize database as well as maintaining rules and restriction.
        DATABASE MODULES took care of the operation.
    WHEN: Version 1 written 12-05-2020
    PURPOSE: 
        To define all data definition used in the app.
'''

from .db import get_db
from enum import Enum
from datetime import date
from flask_login import UserMixin
from . import login_manager

db = get_db()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# manually created tables needed for many-to-many relationship
group_admin = db.Table('group_admin',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True))
group_mate = db.Table('group_mate',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True))
trip_host = db.Table('trip_host',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'), primary_key=True))
trip_participant = db.Table('trip_participant',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                            db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'), primary_key=True))
trip_pending_participant = db.Table('trip_pending_participant',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                            db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'), primary_key=True))


class Gender(Enum):
    Male = 1
    Female = 2
    TransMale = 3
    TransFemale = 4
    Genderqueer = 5
    SomethingElse = 6


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    birthday = db.Column(db.Date(), nullable=False)
    rating = db.relationship('Rating', uselist=False, backref='user')
    mate_of_groups = db.relationship('Group', secondary=group_mate)
    admin_of_groups = db.relationship('Group', secondary=group_admin)
    nationality = db.Column(db.String(64))  # to be changed
    languages = db.Column(db.String(64))  # to be changed
    email = db.Column(db.String(64), nullable=False)
    photo = db.Column(db.LargeBinary(length=2**32 - 1))
    passport_number = db.Column(db.String(16), nullable=False)
    is_web_admin = db.Column(db.Boolean, nullable=False)
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # initialize associated rating
        self.rating = Rating(user_id=self.id, user=self)
        # calculate age
        today = date.today()
        born = self.birthday
        self.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class Rating(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friendliness = db.Column(db.Float, nullable=False)
    cleanliness = db.Column(db.Float, nullable=False)
    timeliness = db.Column(db.Float, nullable=False)
    foodies = db.Column(db.Float, nullable=False)
    number_of_votes = db.Column(db.Integer, nullable=False)
    # more metric to be implemented

    def __init__(self, **kwargs):
        super(Rating, self).__init__(**kwargs)
        # initialize to all zero
        self.friendliness = 0
        self.cleanliness = 0
        self.timeliness = 0
        self.foodies = 0
        self.number_of_votes = 0


class Group(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(64), nullable=False)
    # accessibility is public or private
    public = db.Column(db.Boolean)
    admins = db.relationship('User', secondary=group_admin)
    mates = db.relationship('User', secondary=group_mate)
    trips = db.relationship('Trip', backref='group')  # ongoing and past trip will be distinguished by Trip.finished instead
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.Integer, nullable=False)

class Trip(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    hosts = db.relationship('User', secondary=trip_host)
    participants = db.relationship('User', secondary=trip_participant)
    pending_participants = db.relationship('User', secondary=trip_pending_participant)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    destination = db.Column(db.String(64), nullable=False)
    budget_max = db.Column(db.Float, nullable=False)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    length = db.Column(db.Interval, nullable=False)
    trip_type = db.Column(db.String(64))  # to be changed
    finished = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, **kwargs):
        super(Trip, self).__init__(**kwargs)
        self.finished = False
