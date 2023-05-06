from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrations = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth_routes.login_page'
