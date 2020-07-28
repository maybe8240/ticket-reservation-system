
from flask import render_template, request, url_for

from app.forms.search_order import SearchForm
from . import web


@web.route('/')
def index():
    form = SearchForm(request.form)
    form.single_double.default = 'Round-Trip'
    form.process()
    return render_template('web/index.html', form=form)

import os
from flask import send_from_directory

@web.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(web.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon') #sign for ico file

