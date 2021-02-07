from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.models import User, CustomCard, CustomPalette
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, InternalServerError

import json


class CustomCardApi(Resource):
    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            custom_cards = CustomCard.objects(author=user).to_json()
            return Response(custom_cards, mimetype="application/json", status=200)
        except (FieldDoesNotExist, ValidationError, InvalidQueryError):
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            custom_card = CustomCard(**body, author=user)
            custom_card.save()
            user.update(push__custom_cards=custom_card)
            user.save()
            response = {'id': custom_card.id}
            return Response(json.dumps(response), mimetype="application/json", status=200)
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError

class CustomPaletteApi(Resource):
    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            custom_palettes = CustomPalette.objects(author=user).to_json()
            return Response(custom_palettes, mimetype="application/json", status=200)
        except (FieldDoesNotExist, ValidationError, InvalidQueryError):
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            custom_palette = CustomPalette(**body, author=user)
            custom_palette.save()
            user.update(push__custom_palettes=custom_palette)
            user.save()
            response = {'id': custom_palette.id}
            return Response(json.dumps(response), mimetype="application/json", status=200)
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError
