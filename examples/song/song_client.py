import datetime

from examples.song.factory import ElasticSearchFactory
from examples.song.song import Song

factory = ElasticSearchFactory(os.environ.get('ES_HOST'), os.environ.get('ES_PORT'))
es_client = factory.create()
Song.having(es=es_client)
Song.init()

sour = Song()
sour.name = "Sour"
sour.rating = 0
sour.artist = {
    "name": "Void Vision",
    "bio": "Some Bio"
}
sour.genres = [
    "synth-pop",
    "New Wave"
]
sour.album = {
    "name": "Sub Rosa",
    "year": 2014
}

sour.created = datetime.datetime.utcnow().isoformat()

sour.save()
