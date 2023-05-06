from flask import render_template, redirect, url_for, abort, Blueprint
from flask_login import current_user, login_required

from app.services.room_services import get_room_messages, room_is_exist, create_room
from app.services.user_services import get_recipient_by_sender_id


bp = Blueprint('chat_routes', __name__, url_prefix='/chat',
               template_folder='templates')


@bp.route('/create_chat_room/<int:recipient_id>')
@login_required
def create_chat_room(recipient_id: int):
    '''Создание комнаты или редирект в
    уже существующую'''

    # Если пользователь хочет создать комнату с
    # самим собой - выкидываем ошибку
    if recipient_id == current_user.id:
        abort(404)
    
    # Для начала нужно проверить, не существует ли уже такая комната

    # Определяем два возможных названия комнаты
    room_name_variant_1 = str(current_user.id) + ":" + str(recipient_id)
    room_name_variant_2 = str(recipient_id) + ":" + str(current_user.id)

    # Проверяем первый вариант
    room_is_exist_1 = room_is_exist(room_name=room_name_variant_1)

    # Проверяем второй вариант
    room_is_exist_2 = room_is_exist(room_name=room_name_variant_2)

    if room_is_exist_1:
        return redirect(url_for('chat_routes.chat_room', room_name=room_name_variant_1))
    
    elif room_is_exist_2:
        return redirect(url_for('chat_routes.chat_room', room_name=room_name_variant_2))

    # Если комнаты не существует создаем новую
    else:
        create_room(room_name_variant_1)

        return redirect(url_for('chat_routes.chat_room', room_name=room_name_variant_1))


@bp.route('/chat_room/<string:room_name>')
@login_required
def chat_room(room_name):
    '''Комната чата'''

    # Получаем собеседника
    recipient = get_recipient_by_sender_id(room_name=room_name,
                                sender_id=current_user.id,)

    # Получаем список всех сообщений комнаты
    room_messages = get_room_messages(room_name=room_name)

    return render_template(
        'chat/chat_room.html',
        room_messages=room_messages,
        other_user_username=recipient.username,
        room_name=room_name,
        )
