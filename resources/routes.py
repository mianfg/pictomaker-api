from .language import LanguageApi, LanguageDetectorApi


def initialize_routes(api):
    api.add_resource(LanguageApi, '/api/language')
    api.add_resource(LanguageDetectorApi, '/api/language/detect')
