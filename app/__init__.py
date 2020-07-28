from flask import Flask, url_for, session
from flask_login import LoginManager
from flask_s3 import FlaskS3
import flask_s3
from werkzeug.security import generate_password_hash
from app.config import db

from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config')

    # init flask-s3 to upload static file
    s3 = FlaskS3()
    s3.init_app(app)
    app.config['FLASKS3_BUCKET_NAME'] = 'a2homework'
    #flask_s3.create_all(app)

    register_blueprint(app)

    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = 'Please login or register'

    admin_t = db.Table('admin')
    response = admin_t.scan(
        FilterExpression=Attr('nickname').eq('admin')
    )
    items = response['Items']
    if not len(items):
        admin_t.put_item(
            Item={
                'nickname': 'admin',
                'role': 'super',
                'password': generate_password_hash('123456'),
                'create_time': int(datetime.now().timestamp())
            }
        )

    return app


def register_blueprint(app):
    from app.web import web
    from app.admin import admin
    app.register_blueprint(admin)
    app.register_blueprint(web)
