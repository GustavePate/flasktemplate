from flasktemplate.services.model.UserModel import UserModel
from flask_restful_swagger_2 import Resource
from flask_restful_swagger_2 import swagger


class ExempleResource(Resource):

    @swagger.doc({
        'tags': ['user'],
        'description': 'Returns a user',
        'parameters': [
            {
                'name': 'user_id',
                'description': 'User identifier',
                'in': 'path',
                'type': 'integer'
            }
        ],
        'responses': {
            '200': {
                'description': 'User',
                'schema': UserModel,
                'examples': {
                    'application/json': {
                        'id': 1,
                        'name': 'somebody'
                    }
                }
            }
        }
        })
    def get(self, user_id):
        # Do some processing
        # generates json response {"id": 1, "name": "somebody"}
        return UserModel(id=1, name='somebody'), 200
