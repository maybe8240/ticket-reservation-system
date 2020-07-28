
from wtforms import StringField, PasswordField, Form
from wtforms.validators import Length,ValidationError, EqualTo,DataRequired


class LoginForm(Form):
    nickname = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter your password.')])


class RegisterForm(Form):
    nickname = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                               EqualTo('repeat_password')])
    repeat_password = PasswordField('Confirm Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    id_card = StringField('ID Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])



class ChangeInfoForm(Form):
    nickname = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    name = StringField('Name', validators=[DataRequired()])
    id_card = StringField('ID Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
