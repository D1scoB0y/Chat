from flask import current_app as app
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User, BlackList


def get_user_by_id(user_id: int) -> User | None:
    '''Достаем пользователя по id'''

    with app.app_context():

        user = User.query.get(user_id)

        return user


def get_user_by_username(username: str) -> User | None:
    '''Поиск пользователя по имени'''

    with app.app_context():

        user = User.query.filter_by(username=username)\
            .first()
        
        return user


def user_is_exist(username: str) -> bool:
    '''Проверка пользователя на существование
    True если пользователь существует'''

    user = get_user_by_username(
        username=username,
    )

    return user is not None


def get_recipient_id_by_sender_id(
        room_name: str, sender_id: str,
    ) -> int:
    
    recipient_id = room_name.replace(str(sender_id), '')\
        .replace(':', '')
    
    return recipient_id


def get_recipient_by_sender_id(room_name: str,
        sender_id: int) -> User:
    '''Поиск получателя сообщения, исходя из
    имени комнаты и имени отправителя'''

    recipient_id = get_recipient_id_by_sender_id(
        room_name=room_name,
        sender_id=sender_id,
    )

    return get_user_by_id(recipient_id)


def user_in_blacklist(blacklist_owner_id: int, user_id: int) -> bool:
    '''Проверяет находится ли пользователь в
    черном списке у другого пользователя
    Если находится возвращает True'''

    with app.app_context():

        blacklist_record = BlackList.query.filter_by(blacklist_owner_id=blacklist_owner_id)\
        .filter_by(user_id=user_id).first()

        return blacklist_record is not None


def search_users_by_username_part(username_part: str) -> dict:
    '''Подбирает доступных пользователей по части их имени
    (поиск пользователя по имени на главной странице)'''

    with app.app_context():

        variants = User.query.with_entities(User.id, User.username)\
            .filter(User.username.ilike(username_part + '%'))\
                .limit(8).all()
        
        variants = list(map(list, variants))
        
        
        if current_user.username in variants:
            variants.remove(current_user.username)

        return {
            'data': variants,
        }


def change_username(user_id: int, new_username: str) -> None:
    '''Изменение имени пользователя'''

    with app.app_context():

        user = User.query.get(user_id)

        user.username = new_username

        db.session.add(user)
        db.session.commit()


def create_user(username: str, password: str) -> None:
    '''Создание нового пользоватля'''
    
    with app.app_context():

        new_user = User(
            username=username,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()


def user_login(username: str, password: str, remember: bool) -> bool:
    '''Авторизация пользователя по имени и паролю'''

    with app.app_context():

        # поиск пользователя по имени
        user = get_user_by_username(username=username)

        # Проверяем найден ли пользователь и подходит ли пароль
        if user is not None and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return True
        
        return False

