import random

from datetime import datetime

from . import db
from .error_handlers import InvalidAPIUsage
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
        for _ in range(length):
            return ''.join(random.choices(Constants.SYMBOLS, k=length))

    def save(self):
        if not self.original:
            raise InvalidAPIUsage('Оригинальная длинная ссылка '
                                  'не может быть пустой.')
        if not self.short:
            self.short = self.get_unique_short_id()
        elif URLMap.get(self.short):
            raise InvalidAPIUsage(
                f'Предложенный вариант короткой ссылки "{self.short}" '
                f'уже существует.')
        db.session.add(self)
        db.session.commit()