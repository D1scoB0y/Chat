import datetime as dt

from app import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)

    msg_user = db.relationship('Messages', backref='sender', lazy='dynamic')

    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    email_is_verified = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class BlackList(db.Model):
    __tablename__  = 'BlackList'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)
    banned_user_id = db.Column(db.Integer, nullable=False)
    
    def __init__(self, user_id, banned_user_id):
        self.user_id = user_id
        self.banned_user_id = banned_user_id


class ChatRoom(db.Model):
    __tablename__ = 'ChatRoom'

    id = db.Column(db.Integer, primary_key=True)

    room_name = db.Column(db.String, nullable=False, unique=True)
    last_message_sender = db.Column(db.String)
    last_message_text = db.Column(db.String)
    last_message_date = db.Column(db.DateTime)

    def __init__(self, room_name):
        self.room_name = room_name


class Messages(db.Model):
    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    msg_type = db.Column(db.String, nullable=False)
    sender_username = db.Column(db.String, nullable=False)
    room_name = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    send_date = db.Column(db.DateTime, nullable=False)
    only_for = db.Column(db.String, nullable=False)

    def __init__(self, sender_username, msg_type, sender_id, room_name, text, send_date, only_for):

        self.sender_id = sender_id
        self.sender_username = sender_username
        self.msg_type = msg_type
        self.room_name = room_name
        self.text = text
        self.send_date = send_date
        self.only_for = only_for

    def like_json(self):
        return {
            'sender_username':self.sender_username,
            'room_name':self.room_name,
            'text':self.text,
            'send_date':self.send_date.strftime('%H:%M %d.%m.%Y'),
        }


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
