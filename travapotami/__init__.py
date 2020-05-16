'''
    INIT MODULE: Module to create the application instance and packs the whole application as a Python package.
    PROGRAMMER: Chaichon Wongkham, Chaiyasait Prachaseree
    CALLING SEQUENCE: Access automatically by flask when the app start
    WHEN: Version 1 written 12-05-2020
    PURPOSE: 
        This module composed of the 'application factory' to create the application instance.
        It also packs the whole application as a Python package for better organization.
'''
import os
from flask import Flask, render_template
from . import db
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from .admin_views import MyModelView


login_manager = LoginManager()
bcrypt = Bcrypt()

'''
    CREATE_APP: This function is flask's 'application factory', return the app instance for an execution.
    CALLING SEQUENCE: Automatically called by flask when start the app.
    PURPOSE: To set necessary configurations and registering app components with the app instance before returning it.
    DATA STRUCTURE: Flask's application object.
    ALGORITHM:
        Configure the app.
        Check if there are test configurations and load it.
        Registering CLI commands with the app.
        Register all the blueprints with the app.
        Register all database models with the app.
'''
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='mysql://admin:admin@localhost/travapotami',
        # for debugging
        SQLALCHEMY_ECHO=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app_command(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    admin = Admin(app)
    
    
    with app.app_context():
        from .auth import auth_blueprint
        from .main import main_blueprint
        from .group import group_blueprint
        from .trips import trips_blueprint
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(main_blueprint)
        app.register_blueprint(group_blueprint)
        app.register_blueprint(trips_blueprint)
        @app.errorhandler(404)
        def page_not_found(e):
            return render_template('404.html'), 404
        from .models import User, Group, Trip, Rating
        dbs = db.get_db()
        admin.add_view(MyModelView(User, dbs.session))
        admin.add_view(MyModelView(Group, dbs.session))
        admin.add_view(MyModelView(Trip, dbs.session))
        admin.add_view(MyModelView(Rating, dbs.session))
    return app
