from flask_socketio import leave_room, emit, join_room
from flask_login import current_user
import datetime as dt 

from app import socketio, db
from app.models import User, Messages, ChatRoom, BlackList


@socketio.on('connect_to_room')
def room_joining(data):

    join_room(data['room_name'])
    join_room(current_user.username)


@socketio.on('disconnect_from_room')
def room_leaving(data):

    leave_room(data['room_name'])
    leave_room(current_user.username)


@socketio.on('new_command')
def new_message(data):

    room = ChatRoom.query.filter_by(room_name=data.get('room_name')).first()

    # Определяем отправителя
    sender = User.query.filter_by(username=data.get('sender_username')).first()

    # Определяем получателя
    receiver_username = data.get('room_name').replace(sender.username, '').replace(':', '')
    receiver = User.query.filter_by(username=receiver_username).first()

    #Проверяем не находится ли отправитель в черном списке
    receiver_in_black_list = BlackList.query.filter(BlackList.user_id==sender.id)\
        .filter(BlackList.banned_user_id==receiver.id).first() is not None


    # Проверяем команду на добавление в черный список
    if data.get('message_text') == '/ban':

        # Если 'другой' человек уже в списке просто напоминаем об этом пользователю который
        # хочет повторно отправить туда 'другого' пользователя
        if receiver_in_black_list:

            new_message = Messages(
                sender_id=sender.id,
                sender_username='System',
                msg_type='command',
                room_name=room.room_name,
                text=f'{receiver.username} is already on your blacklist',
                send_date=dt.datetime.now().replace(microsecond=0),
                only_for=sender.username
            )

            db.session.add(new_message)

        # Если не в списке, добавляем его туда
        else:

            new_banned_user = BlackList(
                user_id=sender.id,
                banned_user_id=receiver.id,
            )

            new_message = Messages(
                sender_id=sender.id,
                sender_username='System',
                msg_type='command',
                room_name=room.room_name,
                text=f'You have added {receiver.username} to the blacklist,\
                        to resume the ability to send messages, enter the command "/unban"',
                send_date=dt.datetime.now().replace(microsecond=0),
                only_for=sender.username
            )

            db.session.add_all([new_banned_user, new_message])

        db.session.commit()

        emit('new_command',
            {
                'message_type':'command',
                'message_obj':new_message.like_json(),
            },
            room=sender.username,
            broadcast=True
        )


    # Проверяем команду на удаление из черного списка
    elif data.get('message_text') == '/unban':

        if not receiver_in_black_list:

            new_message = Messages(
                sender_id=sender.id,
                sender_username='System',
                msg_type='command',
                room_name=room.room_name,
                text=f'{receiver.username} is not on your blacklist',
                send_date=dt.datetime.now().replace(microsecond=0),
                only_for=sender.username
            )

        else:

            delete_from_blacklist = BlackList.query.filter(BlackList.user_id==sender.id)\
                .filter(BlackList.banned_user_id==receiver.id,).first()
            
            new_message = Messages(
                sender_id=sender.id,
                sender_username='System',
                msg_type='command',
                room_name=room.room_name,
                text=f'You have removed {receiver.username} from your blacklist',
                send_date=dt.datetime.now().replace(microsecond=0),
                only_for=sender.username
            )

            db.session.delete(delete_from_blacklist)

        db.session.add(new_message)
        db.session.commit()

        emit('new_command',
            {'message_type':'command', 'message_obj':new_message.like_json()},
            room=sender.username,
            broadcast=True
        )


    # Команда очистки чата от системных сообщений
    elif data.get('message_text') == '/delete_sys_messages':

        Messages.query.filter_by(
            room_name=data.get('room_name'),
            sender_username='System',
            sender_id=sender.id
        ).delete()

        db.session.commit()

        emit('delete_sys_messages',
            {},
            room=sender.username,
            broadcast=True
        )

    
    # Если команда не найдена
    else: 

        message_text = data.get('message_text')

        new_message = Messages(
                sender_id=sender.id,
                sender_username='System',
                msg_type='command',
                room_name=room.room_name,
                text=f'Command {message_text} does not exist',
                send_date=dt.datetime.now().replace(microsecond=0),
                only_for=sender.username
            )

        emit('new_command',
            {'message_type':'command', 'message_obj':new_message.like_json()},
            room=sender.username,
            broadcast=True
        )


@socketio.on('new_message')
def new_message(data):

    room = ChatRoom.query.filter_by(room_name=data.get('room_name')).first()

    # Определяем отправителя
    sender = User.query.filter_by(username=data.get('sender_username')).first()

    # Определяем получателя
    receiver_username = data.get('room_name').replace(sender.username, '').replace(':', '')
    receiver = User.query.filter_by(username=receiver_username).first()


    #Проверяем не находится ли отправитель в черном списке
    sender_in_black_list = BlackList.query.filter(BlackList.user_id==receiver.id)\
        .filter(BlackList.banned_user_id==sender.id).first() is not None

    #Проверяем не находится ли получатель в черном списке
    receiver_in_black_list = BlackList.query.filter(BlackList.user_id==sender.id)\
        .filter(BlackList.banned_user_id==receiver.id).first() is not None
 
        
    # Проверяем не находится ли отправитель в черном списке у получателя
    if sender_in_black_list:

        new_message = Messages(
            sender_id=sender.id,
            sender_username='System',
            room_name=room.room_name,
            msg_type='command',
            text=f'{receiver.username} has added you to the blacklist',
            send_date=dt.datetime.now().replace(microsecond=0),
            only_for=sender.username,
        )

        db.session.add(new_message)
        db.session.commit()
        emit('new_command', {'message_type':'command', 'message_obj':new_message.like_json()}, room=sender.username, broadcast=True)

    # Проверяем не находится ли получатель в чернои списке у отправителя
    elif receiver_in_black_list:

        new_message = Messages(
            sender_id=sender.id,
            sender_username='System',
            room_name=room.room_name,
            msg_type='command',
            text='To send messages to a user, remove him from your blacklist. Use "/unban" command',
            send_date=dt.datetime.now().replace(microsecond=0),
            only_for=sender.username,
        )

        db.session.add(new_message)
        db.session.commit()
        emit('new_command', {'message_type':'command', 'message_obj':new_message.like_json()}, room=sender.username, broadcast=True)

    # Если все нормально - отправляем обычное сообщение 
    else:

        new_message = Messages(
            sender_id=sender.id,
            sender_username=sender.username,
            room_name=room.room_name,
            msg_type='message',
            text=data.get('message_text'),
            send_date=dt.datetime.now().replace(microsecond=0),
            only_for='all'
        )
        
        room.last_message_sender = sender.username
        room.last_message_text = new_message.text
        room.last_message_date = new_message.send_date

        db.session.add(new_message)
        db.session.commit()
        emit('new_message', {'message_type':'message', 'message_obj':new_message.like_json()}, room=room.room_name, broadcast=True)
