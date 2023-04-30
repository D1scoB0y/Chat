'''Валидаторы форм при регистрации и авторизации'''
from wtforms.validators import ValidationError


from app.forms.error_text import username_not_unique
from app.services.user_services import user_is_exist


def username_is_unique_validator(form, field):
    '''Проверяет имя пользователя на уникальность'''
    if user_is_exist(field.data):
        raise ValidationError(username_not_unique)

