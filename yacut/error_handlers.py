from flask import jsonify, render_template

from . import app, db
from .settings import Constants


class InvalidAPIUsage(Exception):
    status_code = Constants.HTTP_STATUS_BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(Constants.HTTP_STATUS_NOT_FOUND)
def page_not_found(error):
    return render_template('404.html'), Constants.HTTP_STATUS_NOT_FOUND


@app.errorhandler(Constants.HTTP_STATUS_INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    return (render_template('500.html'),
            Constants.HTTP_STATUS_INTERNAL_SERVER_ERROR)
