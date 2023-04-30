from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Приложение flask
app = Flask(__name__)

# Подключение конфига
app.config.from_object('config.Config')

# Инициализация расширений
socketio = SocketIO(app, cors_allowed_origins="*", server='eventlet')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'main_page'

from app import events, routes, models
