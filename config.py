import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    '''Конфигурация приложения'''

    # Секретный ключ
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Конфигурация бд
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # Конфигурация пользователя
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 24

    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 255