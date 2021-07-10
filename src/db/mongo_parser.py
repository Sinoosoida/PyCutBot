from datetime import datetime
from enum import Enum
import mongoengine as mongo
from utils import Singleton, timeit


class Collection(Enum):
    VIDEO = 'video'
    PLAYLIST = 'playlist'
    CHANNEL = 'channel'


class Status(Enum):
    IN_QUEUE = 'in queue'
    DONE = 'done'
    ERROR = 'error'

    # extras:
    PROCESSING = 'processing'


class Video(mongo.Document):
    url = mongo.StringField(required=True)
    new_video_id = mongo.StringField()
    status = mongo.EnumField(Status, default=Status.IN_QUEUE)
    playlists_urls = mongo.ListField(mongo.StringField())

    def __str__(self):
        return str({'url': self.url,
                    'new_video_id': self.new_video_id,
                    'status': self.status,
                    'playlists_urls': self.playlists_urls})


class Playlist(mongo.Document):
    url = mongo.StringField(required=True)
    new_url = mongo.StringField()
    load_all = mongo.BooleanField()

    def __str__(self):
        return str({'url': self.url,
                    'new_url': self.new_url,
                    'load_all': self.load_all})


class Channel(mongo.Document):
    url = mongo.StringField(required=True)
    last_request_datetime = mongo.DateTimeField(default=datetime.min)

    def __str__(self):
        return str({'url': self.url,
                    'last_request_datetime': self.last_request_datetime})


class MongoParser(metaclass=Singleton):
    @timeit
    def __init__(self, db_name='data0', atlas=False, username=None, password=None):
        if atlas:
            host = (
                f"mongodb+srv://{username}:{password}"
                f"@cluster0.nhitr.mongodb.net/myFirst"
                f"Database?retryWrites=true&w=majority"
            )
            mongo.connect(host=host, db=db_name)
        else:
            mongo.connect(db=db_name)
        self.collections = {
            Collection.VIDEO: Video,
            Collection.PLAYLIST: Playlist,
            Collection.CHANNEL: Channel,
        }

    def _get_doc_type(self, collection_name):
        return self.collections.get(Collection(collection_name))

    def get_all(self, collection_name) -> list:
        mongo_doc_type = self._get_doc_type(collection_name)
        if not mongo_doc_type:
            return []
        return list(mongo_doc_type.objects)

    def save(self, collection_name, **kwargs):
        if not kwargs.get("url"):
            return
        mongo_doc_type = self._get_doc_type(collection_name)
        if not mongo_doc_type:
            return
        new_doc: mongo.Document = mongo_doc_type(**kwargs)
        same_docs = mongo_doc_type.objects(url=kwargs["url"])
        if same_docs.count() == 0:
            new_doc.save()

    def set(self, collection_name, **kwargs):
        if not kwargs.get("url"):
            return
        mongo_doc_type = self._get_doc_type(collection_name)
        if not mongo_doc_type:
            return
        docs_to_change = mongo_doc_type.objects(url=kwargs["url"])
        for doc in docs_to_change:
            for attr in kwargs:
                setattr(doc, attr, kwargs[attr])
            doc.save()

    @staticmethod
    def add_playlist_to_video(url, playlist_url):
        videos_list = Video.objects(url__iexact=url)
        if not videos_list:
            return
        video = videos_list[0]
        if playlist_url not in video.playlists_urls:
            video.playlists_urls.append(playlist_url)
            video.save()

    @staticmethod
    def get_videos_with_status(status) -> list:
        return list(Video.objects(status=Status(status)))

    @staticmethod
    def get_video_with_status(status) -> Video:
        res = MongoParser.get_videos_with_status(status)
        if res:
            return res[0]

    def contains(self, collection_name, url, attribute_name) -> bool:
        mongo_doc_type = self._get_doc_type(collection_name)
        if not mongo_doc_type:
            return False
        docs_list = mongo_doc_type.objects(url__iexact=url)
        if not docs_list:
            return False
        doc = docs_list[0]
        return hasattr(doc, attribute_name)

    def get_attr(self, collection_name, url, attribute_name):
        mongo_doc_type = self._get_doc_type(collection_name)
        if not mongo_doc_type:
            return False
        docs_list = mongo_doc_type.objects(url__iexact=url)
        if not docs_list:
            return False
        doc = docs_list[0]
        return getattr(doc, attribute_name)
