#!/usr/bin/python3
# IMPORT
import logging
import json
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#VARIABLES
db = SQLAlchemy()

def create_app():
    settings = json.load(open("../config/settings.json".format(rootpath), 'r'))
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thedefaultpeonsecretkey'
    # Initialise  DB
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{0}:{1}@{2}:5432/{3}".format(settings["db"]["username"],settings["db"]["password"],settings["db"]["hostname"],settings["db"]["database"])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    from .models import User,Permissions
    # create_database(app)
    logging.debug ("----> [ WebApp ] Starting...")

    # URL Handlers
    #  Import url handlers
    from .views import views
    from .auth import auth
    from .opps import opps
    from .finance import finance
    #  Register url handlers
    app.register_blueprint(views, url_prefix='/')  
    app.register_blueprint(auth, url_prefix='/')  
    app.register_blueprint(opps, url_prefix='/')  
    app.register_blueprint(finance, url_prefix='/')  

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app