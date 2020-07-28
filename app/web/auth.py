from flask import render_template, request, redirect, url_for, flash, app, session
from flask_login import login_user, logout_user, current_user, login_required, UserMixin

from app.forms.auth import RegisterForm, LoginForm, ChangeInfoForm
from app.config import db
from . import web
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key, Attr
from app import login_manager
import boto3
from botocore.exceptions import ClientError


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def get_user(uid):
    return User(uid)


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        #judge if there are duplicate user
        user_t = db.Table('user')
        response = user_t.get_item(
            Key={
                'nickname': form.nickname.data
            }
        )
        if response.__contains__('Item'):
            flash('This username has been registered, try another one')
            return render_template('web/SignUp.html', form=form)

        user_t.put_item(
            Item={
                'nickname': form.nickname.data,
                'create_time': int(datetime.now().timestamp()),
                'tname': form.name.data,
                'email': form.email.data,
                'id_card': form.id_card.data,
                'password': generate_password_hash(form.password.data),
            }
        )
        # Replace sender@example.com with your "From" address.
        # This address must be verified with Amazon SES.
        SENDER = "nianchong.wu@mail.utoronto.ca"

        # Replace recipient@example.com with a "To" address. If your account
        # is still in the sandbox, this address must be verified.
        RECIPIENT = form.email.data

        # Specify a configuration set. If you do not want to use a configuration
        # set, comment the following variable, and the
        # ConfigurationSetName=CONFIGURATION_SET argument below.
        CONFIGURATION_SET = "ConfigSet"

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        AWS_REGION = "us-east-1"

        # The subject line for the email.
        SUBJECT = "Welcome to TicketBooking!"

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Dear guest,\r\n"
                     "Welcome to our ticket booking website! "
                     "We hope you can find a new journey in your life."
                     )

        # The HTML body of the email.
        BODY_HTML = """<html>
            <head>Welcome to TicketBooking!</head>
            <body>
              <h1></h1>
              <p>Dear guest,
              <br>Welcome to our ticket booking website!We hope you can find a new journey in your life.

              </p>
            </body>
            </html>
                        """

        # The character encoding for the email.
        CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses', region_name=AWS_REGION)

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
                # If you are not using a configuration set, comment or delete the
                # following line
                #  ConfigurationSetName=CONFIGURATION_SET,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

        return redirect(url_for('web.login'))
    return render_template('web/SignUp.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':  # and form.validate():
        user_t = db.Table('user')
        response = user_t.scan(
            FilterExpression=Attr('nickname').eq(form.nickname.data)
        )
        if len(response['Items']) != 0:
            userc = response['Items'][0]['nickname']
            pw = response['Items'][0]['password']
            if userc and check_password_hash(pw, form.password.data):
                from flask import session
                from datetime import timedelta

                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=30)
                user = User(datetime.now())
                login_user(user, remember=True)
                session['usernickname'] = userc
                next = request.args.get('next')
                if not next:
                    next = url_for('web.personal_info')
                return redirect(next)
            else:
                flash('Account does not exist or wrong password')
        else:
            flash('Account does not exist or wrong password')
    return render_template('web/VIPSignIn.html', form=form)


@web.route('/personalInfo/', methods=['GET', 'POST'])
@login_required
def personal_info():
    form = ChangeInfoForm(request.form)
    if request.method == 'POST': #and form.validate():
        user_t = db.Table('user')
        user_t.update_item(
            Key={
                'nickname': form.nickname.data,
            },
            UpdateExpression='SET tname = :val1, email = :val2, id_card = :val3, password = :val4',
            ExpressionAttributeValues={
                ':val1': form.name.data,
                ':val2': form.email.data,
                ':val3': form.id_card.data,
                ':val4': generate_password_hash(form.password.data)
            }
        )
        flash('Change user information success')
        return redirect(url_for('web.personal_info'))
    user_t = db.Table('user')
    response = user_t.scan(
        FilterExpression=Attr('nickname').eq(session['usernickname'])
    )
    user = response['Items'][0]
    form.nickname.default = user['nickname']
    form.password.default = user['password']
    form.name.default = user['tname']
    form.id_card.default = user['id_card']
    form.email.default = user['email']
    form.process()
    return render_template('web/VIPInfo.html', form=form)

@web.route('/logout')
@login_required
def logout():
    session['auth']=0
    logout_user()
    return redirect(url_for('web.index'))
