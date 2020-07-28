
from datetime import datetime

from flask import render_template, request, redirect, url_for, session
from flask_login import current_user, login_required
import json
from app.data.order import MyOrder
from app.data.ticket import SearchTicket
from app.forms.search_order import SearchForm, OrderForm
from . import web
from boto3.dynamodb.conditions import Key, Attr
import boto3

db = boto3.resource('dynamodb')

@web.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form)
    if request.method == 'POST':  # and form.validate():
        ticket_t = db.Table('ticket')
        response = ticket_t.scan(
            FilterExpression=#Attr('single_double').eq(form.single_double.data) and
                            Attr('depart_city').eq(form.depart_city.data)&
                            Attr('arrive_city').eq(form.arrive_city.data)&
                            Attr('depart_date').eq(str(form.depart_date.data))
        )
        tickets = response['Items']
        tickets = SearchTicket(tickets).tickets
        return render_template('web/SearchResults.html', tickets=tickets, form=form)

    form.single_double.default = 'Round-trip'
    form.process()
    return render_template('web/SearchResults.html', form=form, tickets=[])


@web.route('/order/<plane_id>')
@login_required
def order(plane_id):

    order_id = 'P' + datetime.now().strftime('%Y%m%d%H%M%S')
    form = OrderForm(request.form)
    ticket_t = db.Table('ticket')
    response = ticket_t.scan(
        FilterExpression=Attr('name').eq(plane_id)
    )
    ticket = response['Items'][0]

    form.order_id.default = order_id
    form.route.default = ticket['depart_city'] + '-' + ticket['arrive_city']
    form.depart_time.default = ticket['depart_date'] + '-' + ticket['depart_time']
    form.process()

    session['plane_id']=plane_id
    return render_template('web/OrderInfo.html', form=form)


@web.route('/order/save_order', methods=['POST'])
@login_required
def save_order():
    form = OrderForm(request.form)
    #Get space avaiable
    ticket_t = db.Table('ticket')
    response = ticket_t.scan(
        FilterExpression=Attr('name').eq(session['plane_id'])
    )
    ticket = response['Items'][0]
    ticket_type_order=form.ticket_type.data
    if ticket_type_order == 'First-class':
        num=ticket['first_class_num']
        classnum='first_class_num'
    elif ticket_type_order == 'Business':
        num=ticket['second_class_num']
        classnum = 'second_class_num'
    else:
        num=ticket['third_class_num']
        classnum = 'third_class_num'
    session['no_ticket']=""
    if num == 0:
        session['no_ticket'] = "There are no tickets for the class you choose, please change another class"
        return redirect(url_for('web.order', plane_id=session['plane_id']))
    if request.method == 'POST':  # and form.validate():
        order_t = db.Table('order')
        order_t.put_item(
            Item={
                'uname': session['usernickname'],
                'create_time': int(datetime.now().timestamp()),
                'order_id': form.order_id.data,
                'route': form.route.data,
                'depart_time': form.depart_time.data,
                'ticket_type': form.ticket_type.data,
                'order_status': 'Completed',
                'email': form.email.data,
                'id_card': form.id_card.data,
                'plane_id': session['plane_id']
            }
        )
        #update avaiable space
        ticket_t.update_item(
            Key={
                'name': session['plane_id'],
            },
            UpdateExpression='SET #classnum = :val1',
            ExpressionAttributeNames={
                '#classnum': classnum
            },
            ExpressionAttributeValues={
                ':val1': num-1
            }
        )
        address = 'http://api.qrserver.com/v1/create-qr-code/?data='+form.order_id.data+form.id_card.data+'&size=100x100'
        client = boto3.client('ses', region_name='us-east-1')
        response = client.update_template(
            Template={
                'TemplateName': 'TEMPLATE',
                'SubjectPart': 'Your Reservation is Confirmed!',
                'TextPart': 'Dear {{name}},we are pleased to tell you that your reservition is confirmed! This is your certification: {{address}} ',
                'HtmlPart': """<html>
                                <p>Dear {{name}},
                                <br>we are pleased to tell you that flight {{flight}} is confirmed for you!
                                <br>Details:
                                <br>Passenger: {{name}}
                                <br>Route: {{route}}
                                <br>Departure time: {{depart_time}}
                                <br>Type: {{type}}
                                <br>Order Status: Comfirmed
                                <br>Click <a href={{address}}>here</a> to download the QR code to check in.
                                </p>
                                </body>
                                </html>
                                """
            }
        )
        data = {'name':session['usernickname'],
                'route':form.route.data,
                'flight':session['plane_id'],
                'depart_time': form.depart_time.data,
                'type': form.ticket_type.data,
                'address':address}
        data_str = json.JSONEncoder().encode(data)
        email = client.send_templated_email(
            Source='nianchong.wu@mail.utoronto.ca',
            Destination={
                'ToAddresses': [
                    form.email.data,
                ],
            },
            Tags=[
                {
                    'Name': 'name',
                    'Value': 'value'
                },
            ],
            Template='TEMPLATE',
            TemplateData= data_str
        )
        print(email)

        return redirect(url_for('web.my_order'))


@web.route('/order/my')
@login_required
def my_order():
    order_t = db.Table('order')
    response = order_t.scan(
        FilterExpression=Attr('uname').eq(session['usernickname'])
    )
    order = response['Items']
    my_order = MyOrder(order).order
    return render_template('web/MyTicket.html', my_order=my_order)
