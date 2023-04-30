from flask_socketio import emit

from app import app, db
from app.models import Message
from app.utils import current_datetime
from app.services.room_services import get_room_by_name
from app.services.user_services import get_user_by_username, get_recipient_by_sender_username,\
    user_in_blacklist, get_recipient_username_by_sender_username as get_recipient_username


def create_system_message(room_name: str, text: str, only_for: str) -> Message:
    '''Создание системного сообщения'''

    with app.app_context():

        message = Message(
            sender_id=1,
            sender_username='System',
            room_name=room_name,
            msg_type='command',
            text=text,
            only_for=only_for,)
        
        db.session.add(message)
        db.session.commit()

        return message


def send_system_message(message: Message) -> None:
    '''Отправка системного сообщения'''

    message = db.session.merge(message)

    with app.app_context():
        emit('new_command',
            {'message_type':'command', 'message_obj':message.like_json()},
            room=message.only_for,
            broadcast=True,)


def create_user_message(sender_id: int, sender_username: str,
    room_name: str, msg_type: str, text: str, only_for: str) -> Message:
    '''Создание пользовательского сообщения'''

    with app.app_context():

        message = Message(
            sender_id=sender_id,
            sender_username=sender_username,
            room_name=room_name,
            msg_type=msg_type,
            text=text,
            only_for=only_for,)
        
        db.session.add(message)
        db.session.commit()

        return message


def send_user_message(message: Message) -> None:
    '''Отправка пользовательского сообщения'''

    with app.app_context():

        message = db.session.merge(message)

        # отправляем сообщение
        emit('new_user_message',
            {'message_type':'message', 'message_obj':message.like_json()},
            room=message.room_name,
            broadcast=True)

        # Если получатель не находится в комнате чата, он все равно сможет
        # увидеть последнее сообщение чата на главной странице
        recipient_username = get_recipient_username(
            room_name=message.room_name,
            sender_username=message.sender_username,
        )
        # отправлем сообщение в комнату в которой находиться
        # получатель если он находиться на главной странице
        emit('new_main_page_message',
            {'message_type':'message', 'message_obj':message.like_json()},
            room='main_page_' + recipient_username,
            broadcast=True)


def update_room_last_message_info(room_name: str, sender_username: str, text: str) -> None:
    '''Обновление данных последнего сообщения комнаты'''

    with app.app_context():

        room = get_room_by_name(room_name=room_name)

        room.last_message_sender = sender_username
        room.last_message_text = text
        room.last_message_date = current_datetime()

        db.session.add(room)
        db.session.commit()


def message_controller(message_data: dict) -> None:
    '''Главный контроллер сообщений'''

    # определяем комнату
    room = get_room_by_name(
        room_name=message_data.get('room_name'),
    )

    # Определяем отправителя
    sender = get_user_by_username(
        username=message_data.get('sender_username'),
    )

    # Определяем получателя
    recipient = get_recipient_by_sender_username(
        room_name=room.room_name,
        sender_username=sender.username,
    )

    # Проверяем находится ли отправитель в черном списке у получателя
    sender_in_black_list = user_in_blacklist(
        blacklist_owner_id=recipient.id,
        user_id=sender.id,
    )

    # Проверяем находится ли получатель в черном списке у отправителя
    recipient_in_black_list = user_in_blacklist(
        blacklist_owner_id=sender.id,
        user_id=recipient.id,
    )

    # Если отправитель в черном списке у получателя
    if sender_in_black_list:
        
        # Отправляем системное сообщение о том, что
        # отправитель находиться в черном списке получателя
        send_system_message(create_system_message(
                room_name=room.room_name,
                text=f'{recipient.username} has added you to the blacklist',
                only_for=sender.username,
            ))

    # Если получатель в черном списке у отправителя
    elif recipient_in_black_list:

        # Отправляем системное сообщение о том, что
        # получатель находиться в черном списке отправителя
        send_system_message(create_system_message(
                room_name=room.room_name,
                text=f'''{recipient.username} is on your blacklist. 
                Use /unban command to delete {recipient.username} 
                from your blacklist''',
                only_for=sender.username,
            ))

    # Если все нормально - отправляем обычное сообщение 
    else:

        update_room_last_message_info(room_name=room.room_name,
                                    sender_username=sender.username,
                                    text=message_data.get('message_text'))

        send_user_message(create_user_message(
            sender_id=sender.id,
            sender_username=sender.username,
            room_name=room.room_name,
            msg_type='message',
            text=message_data.get('message_text'),
            only_for='all',
        ))
