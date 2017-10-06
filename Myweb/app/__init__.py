from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstarp = Bootstrap()
moment = Moment()
db = SQLAlchemy()

'''create_app() function is the appli‐
cation factory, which takes as an argument the name of a configuration to
use for the application'''

def create_app(config_name):
    app = Flask(__name__)

    '''configuration settings
    stored in one of the classes defined in config.py can be imported into
    the application using the from_object()'''

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstarp.init_app(app)
    moment.init_app(app)
    db.init_app(app)



    # attach routes and custom error pages here

    '''single-script applications, the application instance exists
        in the global scope, so routes can be
        easily defined using the app.route decorator.
        But now that the application is created at
        runtime, the app.route decorator begins to exist
        only after create_app() is invoked,
        which is too late'''

    '''Luckily Flask offers a better solution using blueprints.
        A blueprint is similar to an application in that it can also
        define routes. The difference is that routes associated with
        a blueprint are in a dormant state until the blueprint is
        registered with an application,at which point the routes become
        part of it. Using a blueprint defined in the global scope,
        the routes of the application can be defined in almost the
        same way as in the single-script application'''

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
