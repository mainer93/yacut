from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .settings import Constants


class URLForm(FlaskForm):
    original_link = URLField('Длинная ссылка', validators=[DataRequired(
        message='Обязательное поле!'),
        Length(max=Constants.MAX_URL_LENGTH)])
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Regexp(
                Constants.CUSTOM_ID_REGEX,
                message='Короткая ссылка должна содержать '
                'только латинские буквы и цифры и не должна '
                'превышать 16 символов')])
    submit = SubmitField('Создать')
