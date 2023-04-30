from flask import render_template, g, redirect, url_for, flash, abort
from flask_login import current_user, logout_user, login_required

from app import app
from app.forms.forms import RegistrationForm, LoginForm

from app.services.room_services import get_room_messages, get_user_chats, room_is_exist, create_room
from app.services.user_services import search_users_by_username_part, get_recipient_by_sender_username,\
    user_in_blacklist, create_user, user_login


@app.route('/')
def main_page():
    '''Главная страница со списком всех чатов пользователя'''

    if g.user.is_authenticated:
        user_chats = get_user_chats(username=current_user.username)

        return render_template('main_page.html', user_chats=user_chats)
    
    return render_template('main_page.html')


@app.route('/create_chat_room/<string:recipient_username>')
@login_required
def create_chat_room(recipient_username: str):
    '''Создание комнаты чата'''

    # Если пользователь хочет создать комнату с
    # самим собой выкидываем ошибку
    if recipient_username == current_user.username:
        abort(404)
    
    # Для начала нужно проверить, не существует ли уже такая комната

    # Определяем два возможный названия комнаты
    room_name_variant_1 = current_user.username + ":" + recipient_username
    room_name_variant_2 = recipient_username + ":" + current_user.username

    # Проверяем первый вариант
    room_is_exist_1 = room_is_exist(room_name=room_name_variant_1)

    # Проверяем второй вариант
    room_is_exist_2 = room_is_exist(room_name=room_name_variant_2)

    if room_is_exist_1:
        return redirect(url_for('chat_room', room_name=room_name_variant_1))
    
    elif room_is_exist_2:
        return redirect(url_for('chat_room', room_name=room_name_variant_2))

    # Если комнаты не существует создаем новую
    else:
        create_room(room_name_variant_1)

        return redirect(url_for('chat_room', room_name=room_name_variant_1))


@app.route('/chat_room/<string:room_name>')
@login_required
def chat_room(room_name):
    '''Комната чата'''

    # Получаем собеседника
    recipient = get_recipient_by_sender_username(room_name=room_name,
                                sender_username=current_user.username,)

    # Получаем список всех сообщений комнаты
    room_messages = get_room_messages(room_name=room_name)

    # Проверяем нахождение текущего пользователя в черном списке у собеседника
    sender_in_black_list = user_in_blacklist(blacklist_owner_id=recipient.id,
                                                user_id=current_user.id,)

    return render_template(
        'chat_room.html',
        room_messages=room_messages,
        other_user_username=recipient.username,
        room_name=room_name,
        user_in_blacklist=sender_in_black_list,
        )


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    '''Форма регистрации пользователя'''

    form = RegistrationForm()

    if form.validate_on_submit():
        
        # Создание пользователя
        create_user(username=form.username.data,
                    password=form.password.data,)

        # Авторизация пользователя
        user_login(username=form.username.data,
                password=form.password.data,)

        return redirect(url_for('main_page'))


    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    '''Форма авторизации пользователя'''

    form = LoginForm()

    if form.validate_on_submit():
        
        # Авторизация пользователя
        is_logined = user_login(username=form.username.data,
                                password=form.password.data)
        
        # Проверяем подошли ли данные для авторизации
        if is_logined:
            return redirect(url_for('main_page'))
        else:
            flash('Wrong username or password')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    '''Выход из аккаунта'''
    logout_user()

    return redirect(url_for('main_page'))


@app.route('/api/search/<string:username_part>')
def searching(username_part: str) -> None:
    '''Подбирает доступных пользователей по части их имени
    (поиск пользователя по имени на главной странице)'''

    return search_users_by_username_part(username_part=username_part)


@app.errorhandler(404)
def not_found(e):
    '''Хендлер 404 ошибки'''

    return render_template('404.html')


@app.before_request
def g_vars():
    '''g объект'''
    g.user = current_user
