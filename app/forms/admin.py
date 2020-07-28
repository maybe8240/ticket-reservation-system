from wtforms import StringField, PasswordField, Form, SelectField, SubmitField, RadioField, DateField, DateTimeField, \
    HiddenField, IntegerField
from wtforms.validators import Length, Email, ValidationError, EqualTo, Required,DataRequired
import boto3

db = boto3.resource('dynamodb')


class AdminLoginForm(Form):
    nickname = StringField('Usermane', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class AddTicketForm(Form):
    cities = [('Toronto', 'Toronto'), ('Montreal', 'Montreal'), ('Vancouver', 'Vancouver'), ('Edmonton', 'Edmonton'),
              ('Regina', 'Regina'), ('Halifax', 'Halifax'), ('Fredericton', 'Fredericton')]

    id = HiddenField('id')
    submit = SubmitField('Submit')

    name = StringField('IATA', validators=[DataRequired()])
    company_name = SelectField(label="Callsign", validators=[DataRequired("Please choose")])

    depart_city = SelectField("From:", choices=cities, validators=[DataRequired()])
    arrive_city = SelectField("To:", choices=cities, validators=[DataRequired()])

    depart_date = DateField(label='Departure Date', format='%m/%d/%Y', validators=[DataRequired()])
    depart_time = StringField('Departire Time', validators=[DataRequired()])
    arrive_date = DateField(label='Arrival Date', format='%m/%d/%Y', validators=[DataRequired()])
    arrive_time = StringField('Arrival Time', validators=[DataRequired()])

    first_class_price = IntegerField('First Class Price', validators=[DataRequired()])
    second_class_price = IntegerField('Business Class Price', validators=[DataRequired()])
    third_class_price = IntegerField('Economy Class Price', validators=[DataRequired()])
    first_class_num = IntegerField('First Class Ticket Amount', validators=[DataRequired()])
    second_class_num = IntegerField('Business Ticket Amount', validators=[DataRequired()])
    third_class_num = IntegerField('Economy Ticket Amount', validators=[DataRequired()])

    depart_airport = StringField('Departure Airport')
    arrive_airport = StringField('Arrival Airport')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Read company from database
        company_t = db.Table('company')
        response = company_t.scan()
        com = response['Items']
        self.company_name.choices = [(c['company_name'], c['company_name']) for c in com]


class AddAdminForm(Form):
    nickname = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])



class AddCompanyForm(Form):
    En_name = StringField('IATA', validators=[DataRequired()])
    company_name = StringField('Callsign', validators=[DataRequired()])


class ChangeCompanyForm(Form):
    En_name = StringField('IATA', validators=[DataRequired()])
    company_name = StringField('Callsign', validators=[DataRequired()])
