import mongoengine as mongo
from datetime import datetime
from enum import Enum


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


class PlaylistDict(mongo.EmbeddedDocument):
    playlist_url = mongo.StringField()
    uploaded = mongo.BooleanField()

    def __str__(self):
        return str({'playlist_url': self.playlist_url,
                    'uploaded': self.uploaded})


class Video(mongo.Document):
    url = mongo.StringField(required=True)
    new_video_id = mongo.StringField()
    status = mongo.EnumField(Status, default=Status.IN_QUEUE)
    playlists_urls = mongo.ListField(mongo.EmbeddedDocumentField(PlaylistDict))
    status_info = mongo.StringField(default=None)

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
