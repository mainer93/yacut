from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .settings import Constants
from .utils import get_unique_short_id
from .validators import validate_custom_id, validate_url


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    original_url = data.get('url')
    validate_url(original_url)
    custom_id = data.get('custom_id')
    validate_custom_id(custom_id)
    if not custom_id:
        custom_id = get_unique_short_id()
        while URLMap.query.filter_by(short=custom_id).first():
            custom_id = get_unique_short_id()
    new_url = URLMap(original=original_url, short=custom_id)
    db.session.add(new_url)
    db.session.commit()
    short_link = url_for('redirect_to_url', short_id=custom_id, _external=True)
    return (jsonify({'url': original_url, 'short_link': short_link}),
            Constants.HTTP_STATUS_CREATED)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url_mapping = URLMap.query.filter_by(short=short_id).first()
    if url_mapping is None:
        return (jsonify({'message': 'Указанный id не найден'}),
                Constants.HTTP_STATUS_NOT_FOUND)
    return jsonify({'url': url_mapping.original}), Constants.HTTP_STATUS_OK
