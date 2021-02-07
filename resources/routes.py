from .auth import SignupApi, LoginApi
from .custom import CustomCardApi, CustomPaletteApi
from .language import LanguageApi, LanguageDetectorApi
from .training import TrainingApi


def initialize_routes(api):
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

    api.add_resource(CustomCardApi, '/api/custom/card')
    api.add_resource(CustomPaletteApi, '/api/custom/palette')

    api.add_resource(LanguageApi, '/api/language')
    api.add_resource(LanguageDetectorApi, '/api/language/detect')

    api.add_resource(TrainingApi, '/api/training')
