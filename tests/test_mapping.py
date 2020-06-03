from toute import (
    Document, Mapping,
    IntegerField, LongField, KeywordField, FloatField,
    DateField, BooleanField, GeoPointField
)
import json


class BaseDoc(Document):
    _index = 'index'

    @classmethod
    def put_mapping(cls, *args, **kwargs):
        cls.called = True


class Doc(BaseDoc):
    _doctype = 'doc_type'

    integerfield = IntegerField()
    longfield = LongField()
    KeywordField = KeywordField()
    floatfield = FloatField()
    datefield = DateField()
    booleanfield = BooleanField()
    geopointfield = GeoPointField()


class Doc1(BaseDoc):
    _doctype = 'doc_type1'
    integerfield = IntegerField()


class DocDate(Doc):
    datefield = DateField(mapping={'format': 'yyyy-MM-dd||epoch_millis'})


def test_mapping():
    mapping = Mapping(Doc)
    print(mapping.generate())
    assert mapping.generate() == {'doc_type': {
        'properties': {'integerfield': {'type': 'integer'}, 'longfield': {'type': 'long'},
                       'KeywordField': {'index': 'true', 'store': 'true', 'type': 'keyword'},
                       'floatfield': {'type': 'float'}, 'datefield': {'type': 'date'},
                       'booleanfield': {'type': 'boolean'}, 'geopointfield': {'type': 'geo_point'}}}}


def test_change_format():
    mapping = Mapping(DocDate).generate()
    pattern = 'yyyy-MM-dd||epoch_millis'
    assert mapping['doc_type']['properties']['datefield']['format'] == pattern


def test_configure_prerequiriments():
    mapping = Mapping()
    try:
        mapping.configure(10, None)
    except AttributeError as e:
        assert str(e) == 'models_to_mapping must be iterable'


def test_configure_prerequiriments_throw_on_index_existence():
    mapping = Mapping()
    try:
        models = [Doc, Doc1]
        es = ESMock()
        es.indices.exists_ret = True
        mapping.configure(models, True, es)
    except ValueError as e:
        assert str(e) == 'Settings are supported only on index creation'


def test_configure_without_settings():
    mapping = Mapping()
    models = [Doc, Doc1]
    mapping.configure(models, None)
    for model in models:
        assert model.called


def test_configure():
    mapping = Mapping()
    models = [Doc, Doc1]
    es = ESMock()
    es.indices.exists_ret = False
    settings = {
        "asdf": 'This is a test',
        "analyzer": {
            "my_analizer": "Another test"
        }
    }
    mapping.configure(models, settings, es)
    expected_mappings = {
        "doc_type": {
            "properties": {
                "KeywordField": {
                    "index": "true",
                    "store": "true",
                    "type": "keyword"
                },
                "booleanfield": {
                    "type": "boolean"
                },
                "datefield": {
                    "type": "date"
                },
                "floatfield": {
                    "type": "float"
                },
                "geopointfield": {
                    "type": "geo_point"
                },
                "integerfield": {
                    "type": "integer"
                },
                "longfield": {
                    "type": "long"
                }
            }
        },
        "doc_type1": {
            "properties": {
                "integerfield": {
                    "type": "integer"
                }
            }
        }
    }
    expected_output = {
        "settings": settings,
        "mappings": expected_mappings,
    }
    expected_output = json.dumps(expected_output, sort_keys=True, indent=2)
    actual_output = es.indices.create_return['index']
    actual_output = json.dumps(actual_output, sort_keys=True, indent=2)
    print(actual_output)
    assert expected_output == actual_output


class ESMock(object):
    class Indice(object):
        def __init__(self):
            self.create_return = {}

        exists_ret = False

        def exists(self, *args, **kwargs):
            return self.exists_ret

        def create(self, index, body):
            try:
                self.create_return[index] = body
            except:
                self.create_return[index] = body

    indices = Indice()

    def index(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass
