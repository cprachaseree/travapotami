from flask_sqlalchemy import SQLAlchemy
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy(current_app)
    return g.db

def init_db():
    from .models import db, User, Rating, Group, Trip
    #db = get_db()
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

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
    
def init_app_command(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(assign_admin_command)
    app.cli.add_command(remove_admin_command)
