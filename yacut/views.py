from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap
from .settings import Constants
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_url = form.original_link.data
        custom_id = form.custom_id.data or get_unique_short_id()
        if URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        url_map = URLMap(original=original_url, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        short_url = url_for('redirect_to_url', short_id=custom_id,
                            _external=True)
        return render_template('index.html', form=form, short_url=short_url)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_to_url(short_id):
    url_mapping = URLMap.query.filter_by(short=short_id).first()
    if url_mapping:
        return redirect(url_mapping.original)
    return render_template('404.html'), Constants.HTTP_STATUS_NOT_FOUND
