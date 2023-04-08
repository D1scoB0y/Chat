from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import dotenv_values

app = Flask(__name__)

config = dotenv_values('.env')

app.config['SECRET_KEY'] = config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']

socketio = SocketIO(app, cors_allowed_origins="*", server='eventlet')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'main_page'

from app import routes, events, models
