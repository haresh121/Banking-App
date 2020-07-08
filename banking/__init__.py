from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from banking.config import Config
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
bcrypt = Bcrypt()
db = SQLAlchemy()
from banking.models import Transaction, Account, Employee, Customer


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    from banking.UserControl.routes import usercontrol
    from banking.UserManagement.routes import usermgmt
    from banking.errors.handlers import errors
    from banking.UserTransacManagement.routes import usertrmgmt
    app.register_blueprint(usercontrol)
    app.register_blueprint(usermgmt)
    app.register_blueprint(usertrmgmt)
    app.register_blueprint(errors)
    return app
