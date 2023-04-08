from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')

app.config['SECRET_KEY'] = 'inw4n05yn0583n08ndsnjbnsjyn'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:zelel228@localhost:5432/chat_db'

socketio = SocketIO(app, cors_allowed_origins="*", server='eventlet')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'main_page'

from app import routes, events, models
