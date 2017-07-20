from flask_restful_swagger_2 import Schema


class EmailModel(Schema):
    type = 'string'
    format = 'email'
