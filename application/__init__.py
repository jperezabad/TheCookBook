"""Initialize app."""
from flask import Flask
from mongoengine import *
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
login = LoginManager(app)
login.login_view = 'login.login'

def create_app():
    """Construct the core application."""

    database = app.config['DB_NAME']
    host = app.config['DB_HOST']
    port = app.config['DB_PORT']
    username = app.config['DB_USER']
    password = app.config['DB_PASSWORD']
    auth_source = app.config['AUTHENTICATION_SOURCE']
    connect(database, host=host, port=port, username=username, password=password, authentication_source=auth_source)

    with app.app_context():
        # Import parts of our application
        from .api import recipes_routes
        from .api import users_routes
        from . import main_routes
        from . import login_routes

        app.register_blueprint(recipes_routes.api)
        app.register_blueprint(users_routes.api)
        app.register_blueprint(main_routes.main)
        app.register_blueprint(login_routes.users)

        return app