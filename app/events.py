from flask_login import current_user
from flask_socketio import leave_room, join_room

from app import socketio
from app.services.message_services import message_controller
from app.services.command_services import command_controller
from app.services.user_services import get_recipient_id_by_sender_id as get_recipient_id


@socketio.on('connect_to_main_page_room')
def room_joining(data: dict) -> None:
    '''При нахождении пользователя на главной странице он находится в комнате
    с названием "main_page_ + current_user.id" это дает возможность обновлять
    последние сообщения каждой комнаты в реальном времени для этого пользователя
    т.к. сообщения собеседника находящегося в комнате чата отправляеются
    одновременно как в комнату чата текущего пользователя так и в его комнату
    если он находится на главной странице'''

    if current_user.is_authenticated:
        join_room('main_page_' + str(current_user.id))


@socketio.on('disconnect_from_main_page_room')
def room_leaving(data: dict) -> None:
    '''При заходе в комнату чата пользователь выходит из комнаты в
    которой он сосотоял находясь на главной странице'''

    if current_user.is_authenticated:
        leave_room('main_page_' + str(current_user.id))


@socketio.on('connect_to_chat_rooms')
def room_joining(data: dict) -> None:
    '''При заходе в комнату чата, пользователь заходит в несколько комнат:

        1. Комната чата (для получения сообщений собеседника).
        Название формируется по следующему принципу:
        <other_user.id + ":" + current_user.id>
        или
        <current_user.id + ":" + other_user.id>

        2. Собственная комната с названием <current_user.id>
        (для получения системныx сообщений для конкретного пользователя)

        3. Комната собеседника находящегося на главной странице'''

    if current_user.is_authenticated:
        recipient_id = get_recipient_id(room_name=data.get('room_name'),
                                            sender_id=current_user.id,)

        join_room(data.get('room_name'))
        join_room(str(current_user.id))
        join_room('main_page_' + str(recipient_id))


@socketio.on('disconnect_from_chat_rooms')
def room_leaving(data: dict) -> None:
    '''При выходе из комнаты чата пользователь покидает все 3
    комнаты в которыx состоял'''

    if current_user.is_authenticated:
        recipient_id = get_recipient_id(room_name=data.get('room_name'),
                                            sender_id=current_user.id,)

        leave_room(data.get('room_name'))
        leave_room(str(current_user.id))
        leave_room('main_page_' + str(recipient_id))


@socketio.on('new_command')
def new_command(command_data: dict) -> None:
    '''Хендлер комманд'''

    command_controller(command_data=command_data)


@socketio.on('new_user_message')
def new_message(message_data: dict) -> None:
    '''Хендлер пользовательского сообщения'''

    message_controller(message_data=message_data)
