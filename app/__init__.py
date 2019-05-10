import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
moment = Moment()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .pizzeria import pizzeria as pizzeria_blueprint
    app.register_blueprint(pizzeria_blueprint)

    # if app.config['LOG_TO_STDOUT']:
    #     stream_handler = logging.StreamHandler()
    #     stream_handler.setLevel(logging.INFO)
    #     app.logger.addHandler(stream_handler)
    # else:
    #     if not os.path.exists('logs'):
    #         os.mkdir('logs')
    #     file_handler = RotatingFileHandler('logs/manage.log',
    #                                        maxBytes=10240, backupCount=10)
    #     file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
    #                                                 '[in %(pathname)s:%(lineno)d]'))
    #     file_handler.setLevel(logging.INFO)
    #     app.logger.info(file_handler)
    #
    # app.logger.setLevel(logging.INFO)
    # app.logger.info('Pizzeria Startup')

    return app
