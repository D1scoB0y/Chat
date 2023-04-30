from sqlalchemy import or_

from app import app, db
from app.models import ChatRoom, Message


def get_room_by_name(room_name: str) -> ChatRoom | None:
    '''Поиск комнаты чата по имени'''
    with app.app_context():

        room = ChatRoom.query.filter_by(room_name=room_name)\
            .first()
        
        return room


def room_is_exist(room_name: str) -> bool:
    '''Проверка комнаты на существование'''

    room = get_room_by_name(
        room_name=room_name,
        )
    
    return room is not None


def get_room_messages(room_name: str) -> list:
    '''Получение всех сообщений комнаты'''

    with app.app_context():

        room_messages = Message.query.filter_by(room_name=room_name)\
            .order_by(Message.send_date).all()
        
        return room_messages


def get_user_chats(username: str):
    '''Получение всех чатов текущего пользователя'''

    with app.app_context():

        user_chats = ChatRoom.query.filter(or_(
                ChatRoom.room_name.ilike(username + ':%'),
                ChatRoom.room_name.ilike('%:' + username)
            )).all()

        print(user_chats)

        return user_chats


def create_room(room_name: str) -> None:
    '''Создание новой комнаты'''

    with app.app_context():

        new_room = ChatRoom(
            room_name=room_name,
        )

        db.session.add(new_room)
        db.session.commit()

