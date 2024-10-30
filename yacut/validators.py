import re

from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .settings import Constants


def validate_url(url):
    if not url:
        raise InvalidAPIUsage('"url" является обязательным полем!')


def validate_custom_id(custom_id):
    if custom_id:
        if (
            len(custom_id) > Constants.MAX_CUSTOM_ID_LENGTH
            or not re.match(Constants.CUSTOM_ID_REGEX, custom_id)
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.')
