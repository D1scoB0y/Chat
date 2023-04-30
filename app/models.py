from flask_login import UserMixin

from app import utils
from config import Config
from app import db, login_manager


class User(db.Model, UserMixin):
    '''Модель пользователя'''

    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(Config.MAX_USERNAME_LENGTH), nullable=False, index=True, unique=True)
    password = db.Column(db.String(Config.MAX_PASSWORD_LENGTH), nullable=False)

    # получаем пользователя через сообщение
    msg_user = db.relationship('Message', backref='sender')

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(user_id)


class BlackList(db.Model):
    '''Модель черного списка'''

    __tablename__  = 'BlackList'

    id = db.Column(db.Integer, primary_key=True)

    # id пользователя КОТОРЫЙ добавляет в черный список
    blacklist_owner_id = db.Column(db.Integer, nullable=False)

    # id пользователя КОТОРОГО добавляют в черный список
    user_id = db.Column(db.Integer, nullable=False)
    
    def __init__(self, blacklist_owner_id: int, user_id: int) -> None:
        self.blacklist_owner_id = blacklist_owner_id
        self.user_id = user_id


class ChatRoom(db.Model):
    '''Модель комнаты чата'''

    __tablename__ = 'ChatRoom'

    id = db.Column(db.Integer, primary_key=True)

    # имя комнаты
    room_name = db.Column(db.String, nullable=False, index=True, unique=True)

    # данные последнего сообщения
    last_message_sender = db.Column(db.String)
    last_message_text = db.Column(db.String)
    last_message_date = db.Column(db.DateTime)

    def __init__(self, room_name: str) -> None:
        self.room_name = room_name


class Message(db.Model):
    '''Модель сообщения'''

    __tablename__ = 'Message'

    id = db.Column(db.Integer, primary_key=True)

    # id отправителя
    sender_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    # тип сообщения ['message' | 'command']
    msg_type = db.Column(db.String, nullable=False)

    # имя отправителя
    sender_username = db.Column(db.String, nullable=False)

    # имя комнаты
    room_name = db.Column(db.String, nullable=False)

    # текст сообщения
    text = db.Column(db.String, nullable=False)

    # дата отправления
    send_date = db.Column(db.DateTime, nullable=False, default=utils.current_datetime())

    # Имя пользователя для которого предназначено собщение
    # (используется для отправки системных сообщений которые
    # должен видеть только один пользователь)
    only_for = db.Column(db.String, nullable=False)

    def __init__(self, sender_username: str, msg_type: str, sender_id: int,
                room_name: str, text: str, only_for: str) -> None:

        self.sender_id = sender_id
        self.sender_username = sender_username
        self.msg_type = msg_type
        self.room_name = room_name
        self.text = text
        self.only_for = only_for


    def like_json(self) -> dict:
        '''Представляет некоторые данные сообщения в виде словаря'''

        return {
            'sender_username':self.sender_username,
            'room_name':self.room_name,
            'text':self.text,
            'send_date':self.send_date.strftime('%H:%M %d.%m.%Y'),
        }
