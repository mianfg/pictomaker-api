from flask import Response, request
from flask_restful import Resource

from database.models import Training
from resources.errors import SchemaValidationError, InvalidLanguageError, InternalServerError
from mongoengine.errors import FieldDoesNotExist, ValidationError

import json


class TrainingApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            training = Training(**body)
            training.save()
            response = {'id': training.id}
            return Response(json.dumps(response), mimetype="application/json", status=200)
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError
