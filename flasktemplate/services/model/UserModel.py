from flask_restful_swagger_2 import Schema
from flasktemplate.services.model.EmailModel import EmailModel


class UserModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64',
        },
        'name': {
            'type': 'string'
        },
        'mail': EmailModel,
    }
    required = ['name']
