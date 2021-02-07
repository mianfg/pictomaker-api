class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class InvalidLanguageError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "InvalidLanguageError": {
        "message": "Language is invalid",
        "status": 400
    }
}
