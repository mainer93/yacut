import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost')


class Constants(object):
    HTTP_STATUS_OK = 200
    HTTP_STATUS_CREATED = 201
    HTTP_STATUS_BAD_REQUEST = 400
    HTTP_STATUS_NOT_FOUND = 404
    HTTP_STATUS_INTERNAL_SERVER_ERROR = 500
    MAX_URL_LENGTH = 2048
    MAX_CUSTOM_ID_LENGTH = 16
    CUSTOM_ID_REGEX = r'^[A-Za-z0-9]+$'
    MAX_LENGTH = 6
