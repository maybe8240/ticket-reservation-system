from flask import render_template, request, redirect, url_for, flash, session

from app.forms.admin import AddAdminForm
from app.forms.auth import LoginForm

from app.config import db
from . import admin

from boto3.dynamodb.conditions import Key, Attr
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    session['auth'] = 0
    form = LoginForm(request.form)
    if request.method == 'POST':
        admin_t = db.Table('admin')
        response = admin_t.scan(
            FilterExpression=Attr('nickname').eq(form.nickname.data)
        )
        if len(response['Items']) != 0:
            ad = response['Items'][0]['password']
            if ad and check_password_hash(ad, form.password.data):
                session['auth'] = 1
                return redirect(url_for('admin.admin_manage'))
        flash('Incorrect admin account or password')
    return render_template('admin/AdminSignIn.html', form=form)


@admin.route('/admin/manage')
def admin_manage():
    if 'auth' not in session:
        return redirect(url_for('admin.login'))
    if not session['auth']:
        return redirect(url_for('admin.login'))
    form = AddAdminForm(request.form)
    admin_t = db.Table('admin')
    response = admin_t.scan()
    admins = response['Items']
    return render_template('admin/AdminManage.html', form=form, admins=admins)


@admin.route('/admin/addAdmin', methods=['GET', 'POST'])
def add_admin():
    if 'auth' not in session:
        return redirect(url_for('admin.login'))
    if not session['auth']:
        return redirect(url_for('admin.login'))
    form = AddAdminForm(request.form)
    admin_t = db.Table('admin')
    response = admin_t.scan()
    admins = response['Items']
    if request.method == 'POST':  # and form.validate():
        admin_t.put_item(
            Item={
                'nickname': form.nickname.data,
                'role': 'super',
                'password': generate_password_hash(form.password.data),
                'create_time': int(datetime.now().timestamp())
            }
        )
        return redirect(url_for('admin.admin_manage'))
    return render_template('admin/AdminManage.html', form=form, admins=admins)


@admin.route('/admin/changeInfo/<nickname>', methods=['GET', 'POST'])
def change_info(nickname):
    if 'auth' not in session:
        return redirect(url_for('admin.login'))
    if not session['auth']:
        return redirect(url_for('admin.login'))
    form = AddAdminForm(request.form)
    form.nickname.default = nickname
    form.process()
    admin_t = db.Table('admin')
    response = admin_t.scan(
        FilterExpression=Attr('nickname').eq(nickname)
    )
    if request.method == 'GET':
        admin_t.delete_item(
            Key={
                'nickname': nickname,
            }
        )
    return redirect(url_for('admin.admin_manage'))

