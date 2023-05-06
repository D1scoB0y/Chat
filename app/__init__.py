from flask import Flask, g
from flask_socketio import SocketIO
from flask_login import current_user

from app.extensions import db, migrations, login_manager
from app.blueprints import api_routes, user_routes, chat_routes, error_handlers, main_routes, auth_routes
from app.services.user_services import get_user_by_id

# Приложение flask
app = Flask(__name__)

# Подключение конфига
app.config.from_object('config.Config')

# Инициализация расширений
socketio = SocketIO(app, cors_allowed_origins="*", server='eventlet')

db.init_app(app)
migrations.init_app(app)
login_manager.init_app(app)

# Регистрация blueprint'ов
app.register_blueprint(api_routes.bp)
app.register_blueprint(user_routes.bp)
app.register_blueprint(chat_routes.bp)
app.register_blueprint(error_handlers.bp)
app.register_blueprint(main_routes.bp)
app.register_blueprint(auth_routes.bp)

# Регистрация jinja фильтров
app.jinja_env.filters['get_user_by_id'] = get_user_by_id

@app.before_request
def g_vars():
    '''g объект'''
    g.user = current_user

from app import events, models
