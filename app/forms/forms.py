from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField
    )

from config import Config
from app.forms.error_text import wrong_username_length, wrong_password_length, blank_field, passwords_dont_match
from app.forms.validators import username_is_unique_validator


class RegistrationForm(FlaskForm):
    '''Форма регистрации'''

    # Имя пользователя
    username = StringField('username', validators=[
        DataRequired(message=blank_field),
        Length(
            min=Config.MIN_USERNAME_LENGTH,
            max=Config.MAX_USERNAME_LENGTH,
            message=wrong_username_length
        ),
        username_is_unique_validator,
    ])

    # Пароль
    password = PasswordField('password', validators=[
        DataRequired(message=blank_field),
        Length(
            min=Config.MIN_PASSWORD_LENGTH,
            max=Config.MAX_PASSWORD_LENGTH,
            message=wrong_password_length
        ),
    ])

    # Подтверждение пароля
    password2 = PasswordField('password2', validators=[
        DataRequired(),
        EqualTo('password', message=passwords_dont_match),
    ])

    # Не выходить из учетной записи
    remember_me = BooleanField('remember_me')

    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    '''Форма авторизации'''

    # Имя пользователя
    username = StringField('username', validators=[
        DataRequired(message=blank_field),
    ])

    # Пароль
    password = PasswordField('password', validators=[
        DataRequired(message=blank_field),
    ])

    # Не выходить из учетной записи
    remember_me = BooleanField('remember_me')

    submit = SubmitField('submit')


class EditUsernameForm(FlaskForm):
    '''Форма смены имени пользователя'''

    # Новое имя пользователя
    new_username = StringField('username', validators=[
        DataRequired(message=blank_field),
        Length(
            min=Config.MIN_USERNAME_LENGTH,
            max=Config.MAX_USERNAME_LENGTH,
            message=wrong_username_length
        ),
        username_is_unique_validator,
    ])

    # Текущий пароль
    current_password = PasswordField('password', validators=[
        DataRequired(message=blank_field),
    ])

    submit = SubmitField('submit')
