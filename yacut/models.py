import random
import re

from datetime import datetime

from . import db
from .error_handlers import CustomModelError
from .settings import Constants


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(Constants.MAX_URL_LENGTH), nullable=False)
    short = db.Column(db.String(Constants.MAX_CUSTOM_ID_LENGTH), unique=True,
                      nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id(length=Constants.MAX_LENGTH):
        return ''.join(random.choices(Constants.SYMBOLS, k=length))

    def validate_url(self):
        if not self.original:
            raise CustomModelError('"url" является обязательным полем!')

    def validate_custom_id(self):
        if self.short:
            if not re.match(Constants.CUSTOM_ID_REGEX, self.short):
                raise CustomModelError(
                    'Указано недопустимое имя для короткой ссылки')
            if URLMap.get(self.short):
                raise CustomModelError(
                    'Предложенный вариант короткой ссылки уже существует.')

    def save(self):
        self.validate_url()
        if not self.short:
            self.short = self.get_unique_short_id()
        self.validate_custom_id()
        db.session.add(self)
        db.session.commit()
