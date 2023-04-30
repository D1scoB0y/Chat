from flask_login import current_user
from flask_socketio import leave_room, join_room


from app import socketio
from app.services.message_services import message_controller
from app.services.command_services import command_controller
from app.services.user_services import get_recipient_username_by_sender_username as get_recipient_username


@socketio.on('connect_to_main_page_room')
def room_joining(data: dict) -> None:
    '''При нахождении пользователя на главной странице он находится в комнате
    с названием "main_page_ + current_user.username" это дает возможность обновлять
    последние сообщения каждой комнаты в реальном времени для этого пользователя
    т.к. сообщения собеседника находящегося в комнате чата отправляеются
    одновременно как в комнату чата текущего пользователя так и в его комнату
    если он находится на главной странице'''
    join_room('main_page_' + current_user.username)


@socketio.on('disconnect_from_main_page_room')
def room_leaving(data: dict) -> None:
    '''При заходе в комнату чата пользователь выходит из комнаты в
    которой он сосотоял находясь на главной странице'''
    leave_room('main_page_' + current_user.username)


@socketio.on('connect_to_chat_rooms')
def room_joining(data: dict) -> None:
    '''При заходе в комнату чата пользователь заходит в несколько комнат:

        1. Комната чата (для получения сообщений собеседника).
        Название формируется по следующему принципу:
        <other_user.username + ":" + current_user.username>
        или
        <current_user.username + ":" + other_user.username>

        2. Собственная комната с названием <current_user.username>
        (для получения системный сообщений для конткретного пользователя)

        3. Комната собеседника находящегося на главной странице'''

    recipient_username = get_recipient_username(
        room_name=data.get('room_name'),
        sender_username=current_user.username,
    ) 

    join_room(data.get('room_name'))
    join_room(current_user.username)
    join_room('main_page_' + recipient_username)


@socketio.on('disconnect_from_chat_rooms')
def room_leaving(data: dict) -> None:
    '''При выходе из комнаты чата пользователь покидает все 3
    комнаты в который состоял'''

    recipient_username = get_recipient_username(
        room_name=data.get('room_name'),
        sender_username=current_user.username,
    )

    leave_room(data['room_name'])
    leave_room(current_user.username)
    leave_room('mp' + recipient_username)


@socketio.on('new_command')
def new_command(command_data: dict) -> None:
    '''Хендлер комманд'''

    command_controller(command_data=command_data)


@socketio.on('new_user_message')
def new_message(message_data: dict) -> None:
    '''Хендлер нового пользовательского сообщения'''

    message_controller(message_data=message_data)
