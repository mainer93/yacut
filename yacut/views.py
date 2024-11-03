from http import HTTPStatus

from flask import flash, redirect, render_template, url_for

from . import app
from .error_handlers import CustomModelError
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        url_map = URLMap(original=form.original_link.data,
                         short=form.custom_id.data)
        try:
            url_map.save()
        except CustomModelError as e:
            flash(e.message)
            return render_template('index.html', form=form)
        short_url = url_for('redirect_to_url', short_id=url_map.short,
                            _external=True)
        return render_template('index.html', form=form, short_url=short_url)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_to_url(short_id):
    if URLMap.get(short_id):
        return redirect(URLMap.get(short_id).original)
    return render_template('404.html'), HTTPStatus.NOT_FOUND
