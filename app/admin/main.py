
from flask import render_template, request

from app.forms.admin import AdminLoginForm
from . import admin

@admin.route('/admin')
def index():
    form=AdminLoginForm(request.form)
    return render_template('admin/AdminIndex.html',form=form)
