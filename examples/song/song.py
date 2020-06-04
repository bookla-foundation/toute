from toute.fields import ObjectField, KeywordField, DateField, ArrayField, FloatField

from toute.document import Document


class Song(Document):
    # meta attributes
    _index = 'songs'
    _doctype = 'song'

    name = KeywordField()
    rating = FloatField()
    artist = ObjectField(properties={
        "name": {"type": "text"},
        "bio": {"type": "text"},
    })
    album = ObjectField(properties={
        "name": {"type": "text"},
        "year": {"type": "integer"},
    })
    genres = ArrayField(KeywordField())
    created = DateField()
