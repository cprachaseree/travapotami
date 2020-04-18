from flask_sqlalchemy import SQLAlchemy
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy(current_app)
    return g.db

def init_db():
    # db = get_db()
    from .models import db, User, Gender, Rating, Group, Trip
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')
    
def init_app_command(app):
    app.cli.add_command(init_db_command)