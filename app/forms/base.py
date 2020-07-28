from flask import request
from wtforms import Form

class BaseForm(Form):
    def __init__(self):
        body_data = request.form.to_dict()
        query_data = request.args.to_dict()
        super(BaseForm, self).__init__(**body_data, **query_data)

    def validate(self):
        pass