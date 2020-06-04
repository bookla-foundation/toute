from elasticsearch import Elasticsearch


class ElasticSearchFactory(object):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def create(self) -> Elasticsearch:
        return Elasticsearch(
            [{'host': self.host, 'port': self.port}], headers={'X-Api-Key': 'xxxxx'}  # optional
        )
