import os
from flask import Flask, render_template
from . import db
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from .admin_views import MyModelView


login_manager = LoginManager()
bcrypt = Bcrypt()

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
