import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


PostgreDataBase = {
    'user': 'postgres',
    'pw': 'nplus12.3',
    'db': 'digiLib',
    'host': 'localhost',
    'port': '5432',
}


webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
webapp.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % PostgreDataBase
db = SQLAlchemy(webapp)
bcrypt = Bcrypt(webapp)
login_manager = LoginManager(webapp)
login_manager.login_view = 'librarians.login'
login_manager.login_message_category = 'info'

migrate = Migrate(webapp, db)
manager = Manager(webapp)
manager.add_command('db', MigrateCommand)

from digiLib.controller.users.routes import users
from digiLib.controller.librarians.routes import librarians

webapp.register_blueprint(users)
webapp.register_blueprint(librarians)
