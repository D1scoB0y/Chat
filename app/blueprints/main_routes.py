from flask import render_template, g, Blueprint
from flask_login import current_user

from app.services.room_services import get_user_chats

bp = Blueprint('main_routes', __name__,
               template_folder='templates')

@bp.route('/')
def main_page():
    '''Главная страница.
    Если пользователь не авторизован ему предлагается две ссылки:
        1. На форму регистрации
        2. На форму входа в аккаунт'''

    if g.user.is_authenticated:
        user_chats = get_user_chats(user_id=current_user.id)

        return render_template('main/main_page.html', user_chats=user_chats)
    
    return render_template('main/main_page.html')
