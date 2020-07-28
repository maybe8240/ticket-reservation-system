
from datetime import datetime
from wtforms import StringField, PasswordField, Form, SelectField, RadioField, DateField
from wtforms.validators import Length, DataRequired


class SearchForm(Form):
    cities = [('Toronto', 'Toronto'), ('Montreal', 'Montreal'), ('Vancouver', 'Vancouver'), ('Edmonton', 'Edmonton'),
              ('Regina', 'Regina'), ('Halifax', 'Halifax'), ('Fredericton', 'Fredericton'), ('Regina', 'Regina')]
    single_double = RadioField('Trip Type', choices=[('One-way', 'One-way'), ('Round-trip', 'Round-trip')])
    depart_city = SelectField("From:", choices=cities, validators=[DataRequired()])
    arrive_city = SelectField("To:", choices=cities, validators=[DataRequired()])
    depart_date = DateField(label='Departure Date', format='%m/%d/%Y', default=datetime.now())
    return_date = DateField(label='Return Date', format='%m/%d/%Y')


class OrderForm(Form):
    order_id = StringField('Order ID', validators=[DataRequired()])
    route = StringField('Route', validators=[DataRequired()])
    depart_time = StringField('Departure Time', validators=[DataRequired()])
    ticket_type = SelectField('Ticket Type', choices=[('Economy', 'Economy'), ('Business', 'Business'), ('First-class', 'First-class')])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    id_card = StringField('ID Number', validators=[DataRequired()])
