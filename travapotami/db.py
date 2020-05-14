'''
    DATABASE MODULE: Module to carry out database-related operations.
    PROGRAMMER: Chaichon Wongkham
    CALLING SEQUENCE: 
        init_db should be issued before the first run of the application. 
        db object is automatically created when app started/
        IT is used by all other modules through get_db throughout the execution of the app.
    WHEN: Version 1 written 12-05-2020
    PURPOSE: 
        This module is to maintain SQLAlchemy db object to carry out database-related operations. 
        Administrator can also create all needed tables and assign/remove admin.
'''

from flask_sqlalchemy import SQLAlchemy
import click
from flask import current_app, g
from flask.cli import with_appcontext

'''
    GET_DB: 
        This function return the db object to carry out database-related operations. 
        It create a new db object if it is not previously created. The db object is stored for the whole lifetime of app execution.
    CALLING SEQUENCE: Called by every module that need SQLAlchemy database operations by getting the db object at the start of the module.
    PURPOSE: Maintain a single db object for every modules throughout the execuation lifetime of the app.
    DATA STRUCTURES: Database being create or return
    ALGORITHM: 
        If db object is not yet in the global scope of the app, create and put in the scope. 
        If it is already present, return that object
'''
def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy(current_app) # g is global scope
    return g.db

'''
    INIT_DB: This function create (initialize) all database table that is defined in module MODELS.
    CALLING SEQUENCE: 
        This should be called before the first run and everytime that the database has been emptied.
        The app would not behave correctly if this is not called.
    PURPOSE: Create all tables as defined in module MODELS.
    DATA STRUCTURES: 
        Classes being import to be recognized
        Database to call initialization function.
    ALGORITHM: 
        Import every class definition before calling SQLAlchemy built-in function to create all table.
        The preceding import is needed for SQLAlchemy to recognize the table.
'''
def init_db():
    from .models import db, User, Rating, Group, Trip #SQLAlchemy required to import
    db.create_all()

'''
    INIT_DB_COMMAND:
        This function is to register INIT_DB to the command line interface.
        INIT_DB function then would be able to issued through flask console.
    CALLING SEQUENCE: same as INIT_DB
    PURPOSE: To ease the operation of INIT_DB, allowing CLI to call.
    DATA STRUCTURE: click object to manipulate CLI
    ALGORITHM: 
        The function simply called INIT_DB. 
        However, it is decorate by @click.command('init-db') to register this function to CLI when command init-db is issued.
        Print out success message when finished.
'''
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

'''
    ASSIGN_ADMIN_COMMAND: This function is to assign the user with the username as provided in parameter to be an admin.
    CALLING SEQUENCE: Call anytime by administrator in the CLI.
    PURPOSE: Promote a user with username as provided in the parameter to be an admin.
    DATA STRUCTURE:
        Database to query user.
        click object to manipulate CLI.
    ALGORITHM: 
        A user with the user provided in the parameter is searched from the database.
        If found, assign the user to be admin and output success message.
        If not found, display error message.
'''
@click.command('assign-admin')
@click.argument('username')
@with_appcontext
def assign_admin_command(username):
    from .models import db, User
    user = User.query.filter_by(username=username).first()
    if user:
        user.is_web_admin = True
        db.session.commit()
        click.echo('Set user as admin.')
    else:
        click.echo('Username does not exist.')

'''
    REMOVE_ADMIN_COMMAND: 
        This function is to remove the user with the username as provided in parameter from being an admin.
        It is a reverse to ASSIGN_ADMIN_COMMAND.
    CALLING SEQUENCE: Call anytime by administrator in the CLI.
    PURPOSE: Demote a user with username as provided in the parameter from being an admin.
    DATA STRUCTURE:
        Database to query user.
        click object to manipulate CLI.
    ALGORITHM: 
        A user with the user provided in the parameter is searched from the database.
        If found, assign the user to not be admin and output success message.
        If not found, display error message.
'''
@click.command('remove-admin')
@click.argument('username')
@with_appcontext
def remove_admin_command(username):
    from .models import db, User
    user = User.query.filter_by(username=username).first()
    if user:
        if user.is_web_admin:
            db.session.delete(user)
            db.session.commit()
            click.echo('Deleted admin user.')
        else:
            click.echo('User is not an admin.')
    else:
        click.echo('Username does not exist.')

'''
    INIT_APP_COMMAND: The function is to formally register INIT_DB_COMMAND, ASSIGN_ADMIN_COMMAND, REMOVE_ADMIN_COMMAND to the CLI.
    CALLING SEQUENCE: Called automatically when app start.
    PURPOSE: Register all CLI functions to the app.
    DATA STRUCTURE: app object to register CLI command to the app.
    ALGORITHM: Call built-in flask function to add all command to CLI.
'''
def init_app_command(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(assign_admin_command)
    app.cli.add_command(remove_admin_command)
