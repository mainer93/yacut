from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    new_url = URLMap(original=data.get('url'), short=data.get('custom_id'))
    new_url.save()
    short_link = url_for('redirect_to_url', short_id=new_url.short,
                         _external=True)
    return (jsonify({'url': data.get('url'), 'short_link': short_link}),
            HTTPStatus.CREATED)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    if not URLMap.get(short_id):
        return (jsonify({'message': 'Указанный id не найден'}),
                HTTPStatus.NOT_FOUND)
    return (jsonify({'url': URLMap.get(short_id).original}),
            HTTPStatus.OK)