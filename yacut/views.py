from http import HTTPStatus

from flask import flash, redirect, render_template, url_for

from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id:
            if URLMap.get(custom_id):
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form)
        else:
            custom_id = URLMap.get_unique_short_id()
        url_map = URLMap(original=form.original_link.data, short=custom_id)
        url_map.save()
        short_url = url_for('redirect_to_url', short_id=custom_id,
                            _external=True)
        return render_template('index.html', form=form, short_url=short_url)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_to_url(short_id):
    if URLMap.get(short_id):
        return redirect(URLMap.get(short_id).original)
    return render_template('404.html'), HTTPStatus.NOT_FOUND
