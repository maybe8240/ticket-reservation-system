
from flask import Blueprint, render_template

# from app.web import user

web = Blueprint('web', __name__)

from app.web import main
from app.web import auth
from app.web import search_order

#Register global error handler, using app_errorhandler
@web.app_errorhandler(404)
def not_found(e):
    return render_template('web/404.html'), 404
