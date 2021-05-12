from flask import Response, request
from flask_restful import Resource

from resources.errors import SchemaValidationError, InvalidLanguageError, InternalServerError

import spacy, json
from googletrans import Translator


nlp = {
    'en_sm' : spacy.load("en_core_web_sm"),
    # 'en_ac' : spacy.load("en_core_web_trf"),
    # 'fr_sm' : spacy.load("fr_core_news_sm"),
    # 'fr_ac' : spacy.load("fr_dep_news_trf"),
    # 'de_sm' : spacy.load("de_core_news_sm"),
    # 'de_ac' : spacy.load("de_dep_news_trf"),
    # 'it_sm' : spacy.load("it_core_news_sm"),
    # 'it_ac' : spacy.load("it_core_news_lg"),
    # 'es_sm' : spacy.load("es_core_news_sm"),
    'es_ac' : spacy.load("es_dep_news_trf")
}

translator = Translator()

class LanguageApi(Resource):
    def get(self):
        keys = [el.split('_') for el in nlp if nlp[el]]
        languages_dict = {}
        for key in keys:
            if key[0] in languages_dict.keys():
                languages_dict[key[0]].append(languages_dict[key[1]])
            else:
                languages_dict[key[0]] = [key[1]]
        languages = [{'language': language, 'variations': [language+'_'+variation for variation in languages_dict[language]]} for language in languages_dict]
        return Response(json.dumps(languages), mimetype="application/json", status=200)

    def post(self):
        try:
            body = request.get_json()
            language = body.get('language')
            text = body.get('text')
            if not text:
                raise SchemaValidationError
            pair = [None, None]
            pairs = []
            for i in range(len(text)):
                if i == 0 or (i > 0 and text[i-1] != '\\'):
                    if text[i] == '[':
                        pair[0] = i
                    elif text[i] == ']':
                        pair[1] = i
                        if pair[0] and pair[1]:
                            pairs.append(pair)
                        pair = [None, None]
            text = list(text)
            for pair in pairs:
                for i in range(pair[0], pair[1]):
                    if text[i] == ' ':
                        text[i] = '\t'
            text = ''.join(text)
            text = text.replace('\\[', '\n0\n')
            text = text.replace('\\]', '\n1\n')
            text = text.replace('[', '')
            text = text.replace(']', '')
            text = text.replace('\n0\n', '[')
            text = text.replace('\n1\n', ']')
            if not language:
                split_text = text.split(' ')
                doc_dict = []
                for word in split_text:
                    if word != '':
                        word = word.replace('\t', ' ')
                        doc_dict.append({'text': word, 'lemma': word, 'pos': 'OTHER'})
            else:
                if language not in nlp.keys() or not nlp[language]:
                    raise InvalidLanguageError
                doc = nlp[language](text)
                doc_dict_separated = []
                temp = []
                for token in doc:
                    temp.append({'text': token.text, 'lemma': token.lemma_, 'pos': token.pos_, 'is_punct': token.is_punct})
                    if token.whitespace_ or (token.i < len(doc) - 1 and not doc[token.i+1].is_punct and not token.is_punct):
                        doc_dict_separated.append(temp)
                        temp = []
                if len(temp) > 0:
                    doc_dict_separated.append(temp)
                doc_dict = []
                for element in doc_dict_separated:
                    text, lemma, pos = "", element[0]['lemma'], element[0]['pos']
                    for item in element:
                        text += item['text']
                        if not item['is_punct']:
                            lemma, pos = item['lemma'], item['pos']
                    doc_dict.append({'text': text, 'lemma': lemma, 'pos': pos})
                for i in range(len(doc_dict)):
                    if i < len(doc_dict) and doc_dict[i]['pos'] == 'SPACE':
                        doc_dict[i]['text'] = doc_dict[i]['text'].replace('\t', ' ')
                        doc_dict[i]['lemma'] = doc_dict[i]['lemma'].replace('\t', ' ')
                        doc_dict[i]['pos'] = ''
                        if i > 0:
                            doc_dict[i]['text'] = doc_dict[i-1]['text'] + doc_dict[i]['text']
                            doc_dict[i]['lemma'] = doc_dict[i-1]['lemma'] + doc_dict[i]['lemma']
                            doc_dict[i]['pos'] = doc_dict[i-1]['pos']
                            del doc_dict[i-1]
                            i -= 1
                        if i < len(doc_dict):
                            doc_dict[i]['text'] += doc_dict[i+1]['text']
                            doc_dict[i]['lemma'] += doc_dict[i+1]['lemma']
                            if doc_dict[i]['pos'] == '' or doc_dict[i]['pos'] == doc_dict[i+1]['pos']:
                                doc_dict[i]['pos'] = doc_dict[i+1]['pos']
                            else:
                                doc_dict[i]['pos'] = 'OTHER'
                            del doc_dict[i+1]
            return Response(json.dumps(doc_dict), mimetype="application/json", status=200)
        except SchemaValidationError:
            raise SchemaValidationError
        except KeyError:
            raise InvalidLanguageError
        except Exception as e:
            raise InternalServerError

class LanguageDetectorApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            text = body.get('text')
            if not text:
                raise SchemaValidationError
            d = translator.detect(text)
            detection = {'language': d.lang, 'confidence': d.confidence}
            return Response(json.dumps(detection), mimetype="application/json", status=200)
        except SchemaValidationError:
            raise SchemaValidationError
        except Exception as e:
            raise InternalServerError
