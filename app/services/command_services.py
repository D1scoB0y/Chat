from flask import current_app as app
from flask_socketio import emit

from app.extensions import db
from app.models import User, Message, BlackList
from app.services.room_services import get_room_by_name
from app.services.message_services import create_system_message, send_system_message, delete_message
from app.services.user_services import get_user_by_username, get_recipient_by_sender_id, user_in_blacklist


def ban_user(blacklist_owner_id: int, user_id: int) -> None:
    '''Добавление пользователя в черный список другого пользователя.
    Добавление в чс представляет из себя создание записи состоящей
    из id пользователя КОТОРЫЙ добавляет в чс и id пользователя
    КОТОРОГО добавляют. Позже будем проверять состоит ли пользователь
    в чс у собеседника путем проверки существования записи
    с заданными id'''

    with app.app_context():

        new_banned_user = BlackList(
            blacklist_owner_id=blacklist_owner_id,
            user_id=user_id
        )

        db.session.add(new_banned_user)
        db.session.commit()


def unban_user(blacklist_owner_id: int, user_id: int) -> None:
    '''Удаление записи о принадлежности пользователя к черному
    списку другого пользователя'''

    with app.app_context():

        blacklist_record_to_delete = BlackList.query\
            .filter_by(blacklist_owner_id=blacklist_owner_id)\
                .filter_by(user_id=user_id).first()
        
        db.session.delete(blacklist_record_to_delete)
        db.session.commit()


def delete_system_messages(room_name: str, sender: User) -> None:
    '''Удаляет системные сообщения для заданной
    комнаты и пользователя'''
    
    # Удаляем сообщения из бд
    Message.query.filter_by(room_name=room_name)\
        .filter_by(only_for=sender.username).filter_by(sender_username='System').delete()
    
    db.session.commit()

    # Отправляем комманду очистки чата на клиент
    emit('delete_sys_messages',
        {},
        room=str(sender.id),
        broadcast=True)


def show_all_commands(message: Message) -> None:
    '''Вывод в чат всех возможных комманд.
    Только для пользователя который ввел "/help" '''

    message = db.session.merge(message)

    # Отправляем комманду на клиент
    emit('help',
        {'message_type':'command', 'message_obj':message.like_json()},
        room=message.only_for,
        broadcast=True,
    )

    delete_message(message=message)


def command_controller(command_data: dict) -> None:
    '''Контроллер комманд'''

    # Определяем комнату
    room = get_room_by_name(
        room_name=command_data.get('room_name'),
    )

    # Определяем отправителя
    sender = get_user_by_username(
        username=command_data.get('sender_username'),
    )

    # Определяем получателя
    recipient = get_recipient_by_sender_id(
        room_name=command_data.get('room_name'),
        sender_id=sender.id,
    )

    #Проверяем не находится ли отправитель в черном списке
    recipient_in_black_list = user_in_blacklist(
        blacklist_owner_id=sender.id,
        user_id=recipient.id,
    )

    # Проверяем команду на добавление в черный список
    if command_data.get('message_text') == '/ban':

        # Если собеседник уже в черном списке отправителя,
        # то напоминаем отправителю об этом
        if recipient_in_black_list:

            send_system_message(create_system_message(
                room_name=room.room_name,
                text=f'{recipient.username} is already on your blacklist',
                only_for=sender.id,
            ))

        # Если собеседник не в черном списке, добавляем его туда
        else:

            # добавляем собеседника в черный список отправителя
            ban_user(
                blacklist_owner_id=sender.id,
                user_id=recipient.id,
            )

            # Отправляем системное сообщение о добавлении пользователя в черный список
            send_system_message(create_system_message(
                room_name=room.room_name,
                text=f'You have added {recipient.username} to the blacklist,\
                        to resume the ability to send messages, enter the command "/unban"',
                only_for=sender.id,
            ))


    # Проверяем команду на удаление из черного списка
    elif command_data.get('message_text') == '/unban':

        # Если получатель в черном списке у отправителя
        if recipient_in_black_list:

            # Удаляем пользователя из черного списка
            unban_user(
                blacklist_owner_id=sender.id,
                user_id=recipient.id,
            )

            # Опеовещаем отправителя о том что удаление
            # из черного списка произошло
            send_system_message(create_system_message(
                room_name=room.room_name,
                text=f'You have removed {recipient.username} from your blacklist',
                only_for=sender.id,
            ))

        # Если получатель не в черном списке у отправителя,
        # то напоминаем отправителю об этом
        else:
            send_system_message(create_system_message(
                room_name=room.room_name,
                text=f'{recipient.username} is not on your blacklist',
                only_for=sender.id,
            ))


    # Проверяем команду очистки чата от системных сообщений
    elif command_data.get('message_text') == '/clear':

        delete_system_messages(room_name=room.room_name,
                                sender=sender,)


    # Проверяем команду показывающую все доступные команды
    elif command_data.get('message_text') == '/help':

        show_all_commands(create_system_message(
                room_name=room.room_name,
                text='',
                only_for=sender.id,
            ))
