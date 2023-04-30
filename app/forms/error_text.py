'''Тексты ошибок при регестрации и авторизации'''
from config import Config


blank_field = 'Fill in this field'


username_not_unique = 'This username is aleady taken'
wrong_username_length = f'Username length: {Config.MIN_USERNAME_LENGTH} to {Config.MAX_USERNAME_LENGTH}'

wrong_password_length = f'Password length: {Config.MIN_PASSWORD_LENGTH} to {Config.MAX_PASSWORD_LENGTH}'
passwords_dont_match = 'Passwords must match'

# При неудачной авторизации
wrong_username_or_password = 'Wrong username or password'



