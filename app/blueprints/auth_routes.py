from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import logout_user, login_required

from app.forms.forms import RegistrationForm, LoginForm
from app.services.user_services import create_user, user_login


bp = Blueprint('auth_routes', __name__, url_prefix='/auth',
               template_folder='templates')


@bp.route('/registration', methods=['GET', 'POST'])
def registration_page():
    '''Форма регистрации пользователя'''

    form = RegistrationForm()

    if form.validate_on_submit():
        
        # Создание пользователя
        create_user(username=form.username.data,
                    password=form.password.data,)

        # Авторизация пользователя
        user_login(username=form.username.data,
                    password=form.password.data,
                    remember=form.remember_me.data,)

        return redirect(url_for('main_routes.main_page'))


    return render_template('auth/registration.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login_page():
    '''Форма авторизации пользователя'''

    form = LoginForm()

    if form.validate_on_submit():
        
        # Авторизация пользователя
        is_logined = user_login(username=form.username.data,
                                password=form.password.data,
                                remember=form.remember_me.data,)
        
        # Проверяем подошли ли данные для авторизации
        if is_logined:
            return redirect(url_for('main_routes.main_page'))
        else:
            flash('Wrong username or password')

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    '''Выход из аккаунта'''
    logout_user()

    return redirect(url_for('main_routes.main_page'))
