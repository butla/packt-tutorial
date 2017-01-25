import json
import uuid

import falcon
from tinydb import TinyDB, Query


DICTIONARY_STORAGE = 'dictionaries.json'

class DictionaryResource:
    def __init__(self):
        self.dictionary_storage = TinyDB(DICTIONARY_STORAGE)

    def on_get(self, req, resp, dict_id):
        dictionary = self.dictionary_storage.search(Query().id == dict_id)
        if dictionary:
            resp.body = json.dumps(dictionary)
        else:
            resp.status = falcon.HTTP_NOT_FOUND


class DictionaryCollectionResource:
    def __init__(self):
        self.dictionary_storage = TinyDB(DICTIONARY_STORAGE)

    def on_post(self, req, resp):
        dictionary_string = req.stream.read()
        dictionary = json.loads(dictionary_string)

        dict_with_id = dictionary.copy()
        dict_with_id['id'] = str(uuid.uuid4())
        self.dictionary_storage.insert(dict_with_id)

        resp.status = falcon.HTTP_CREATED
        resp.body = json.dumps(dict_with_id)
        resp.content_location = '/' + dict_with_id['id']


application = falcon.API()
application.add_route('/', DictionaryCollectionResource())
application.add_route('/{dict_id}', DictionaryResource())