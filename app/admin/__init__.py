from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)

from app.admin import ticket_manage
from app.admin import auth

from app.admin import main

#Register global error handler, using app_errorhandler
@admin.app_errorhandler(404)
def not_found(e):
    return render_template('web/404.html'), 404
