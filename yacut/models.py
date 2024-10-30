from datetime import datetime

from . import db
from .settings import Constants


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(Constants.MAX_URL_LENGTH), nullable=False)
    short = db.Column(db.String(Constants.MAX_CUSTOM_ID_LENGTH), unique=True,
                      nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
