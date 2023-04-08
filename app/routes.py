from flask import render_template, g, redirect, url_for, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User, ChatRoom, Messages, BlackList
from sqlalchemy import or_

'''
    Main page
'''
@app.route('/')
def main_page():

    if g.user.is_authenticated:
        user_chats = ChatRoom.query.filter(or_(
            ChatRoom.room_name.ilike(g.user.username + ':%'),
            ChatRoom.room_name.ilike('%:' + g.user.username)
        )).all()

        return render_template('main_page.html', user_chats=user_chats)
    
    return render_template('main_page.html')


'''
    Creating chat room
'''
@app.route('/create_chat_room/<string:username>')
@login_required
def create_chat_room(username):

    if username == g.user.username:
        abort(404)

    room_name_variant1 = g.user.username + ':' + username
    room_name_variant2 = username + ':' + g.user.username

    # Проверяем существует ли комната c искомым пользователем
    room_is_exist1 = ChatRoom.query.filter_by(room_name=room_name_variant1).all()
    room_is_exist2 = ChatRoom.query.filter_by(room_name=room_name_variant2).all()

    if len(room_is_exist1):
        return redirect(url_for('chat_room', room_name=room_name_variant1))
    
    elif len(room_is_exist2):
        return redirect(url_for('chat_room', room_name=room_name_variant2))

    else:
        new_room = ChatRoom(
            room_name=room_name_variant1,
        )

        db.session.add(new_room)
        db.session.commit()

        return redirect(url_for('chat_room', room_name=room_name_variant1))


'''
    Chat room
'''
@app.route('/chat_room/<string:room_name>')
@login_required
def chat_room(room_name):

    # Получаем 'другого' пользователя
    other_user_username = room_name.replace(g.user.username, '').replace(':', '')
    other_user = User.query.filter_by(username=other_user_username).first()

    room_messages = Messages.query.filter_by(room_name=room_name).all()

    user_in_blacklist = BlackList.query.filter(BlackList.user_id==other_user.id)\
        .filter(BlackList.user_id==g.user.id) is not None

    return render_template(
        'chat_room.html',
        room_messages=room_messages,
        other_user_username=other_user_username,
        room_name=room_name,
        user_in_blacklist=user_in_blacklist,
        )


'''
    Registration
'''
@app.route('/registration', methods=['GET', 'POST'])
def registration_page():

    form = RegistrationForm()

    if form.validate_on_submit():
         
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('main_page'))

    return render_template('registration.html', form=form)


'''
    Login
'''
@app.route('/login', methods=['GET', 'POST'])
def login_page():

    form = LoginForm()

    if form.validate_on_submit():
         
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and check_password_hash(user.password, form.password.data):

            if form.remember_me.data:
                login_user(user, remember=True)

            else:
                login_user(user)

            return redirect(url_for('main_page'))
        else:
            flash('Wrong email or password')

    return render_template('login.html', form=form)


'''
    Logout
'''
@app.route('/logout')
def logout_page():

    logout_user()

    return redirect(url_for('main_page'))


'''
    Endpoint for searching by username
'''
@app.route('/api/search/<string:name_part>')
def searching(name_part):

    variants = User.query.filter(User.username.ilike(name_part + '%')).limit(8).all()
    variants = list(map(lambda x: x.username, variants))
    
    if g.user.username in variants:
        variants.remove(g.user.username)

    return {
        'data' : variants,
        }


'''
    404 handler
'''
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


'''
     Global variables
'''
@app.before_request
def g_vars():
    g.user = current_user
