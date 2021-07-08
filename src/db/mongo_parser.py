import mongoengine as mongo
from abc import abstractmethod, ABCMeta
from utils import Singleton, timeit
from enum import Enum, auto
import time

from datetime import datetime


class Parser(ABCMeta, Singleton):

    # def get(self, name_of_table, link):#
    #     with sql_execute(self.db_name) as cursor:
    #         answer = list(cursor.execute("""SELECT * FROM {} WHERE link = '{}'"""
    #                                      .format(name_of_table, link)))
    #     return answer

    @abstractmethod
    def get_all(self, name_of_table):
        pass

    @abstractmethod
    def get_video_with_status(self, status):
        pass

    @abstractmethod
    def set_status(self, link, status):  #
        pass

    @abstractmethod
    def get_videos_with_status(self, status):
        pass

    @abstractmethod
    def save(self, name_of_table, link, status=None):
        pass

    @abstractmethod
    def clear_db(self, name_of_table=None):
        pass

    @abstractmethod
    def create_db(self):
        pass


class Status(Enum):
    IN_QUEUE = "in queue"
    DONE = "done"
    ERROR = "error"

    # extras:
    PROCESSING = "processing"


class Video(mongo.Document):
    url = mongo.StringField(required=True)
    status = mongo.EnumField(Status, default=Status.IN_QUEUE)
    playlists_urls = mongo.ListField(mongo.StringField())

    def __str__(self):
        return str({'url': self.url,
                    'status': self.status,
                    'playlists_url': self.playlists_urls})


class Playlist(mongo.Document):
    url = mongo.StringField(required=True)

    def __str__(self):
        return str({'url': self.url})


class Channel(mongo.Document):
    url = mongo.StringField(required=True)
    last_request_datetime = mongo.DateTimeField(default=datetime.min)

    def __str__(self):
        return str({'url': self.url,
                    'last_request_datetime': self.last_request_datetime})


class MongoParser(metaclass=Singleton):
    @timeit
    def __init__(self, db_name="data0", atlas=False, username=None, password=None):
        if atlas:
            host = (
                f"mongodb+srv://{username}:{password}"
                f"@cluster0.nhitr.mongodb.net/myFirst"
                f"Database?retryWrites=true&w=majority"
            )
            mongo.connect(host=host, db=db_name)
        else:
            mongo.connect(db=db_name)
        self.collections = {"video": Video, "playlist": Playlist, "channel": Channel}

    def clear_db(self, name_of_table=None):
        if not name_of_table:
            print("no name_of_table specified, exiting")
            return
        print(self.get_all(name_of_table))
        if input("Are you sure? y/n") == "y":
            mongo_doc_type = self.collections.get(name_of_table)
            if not mongo_doc_type:
                return
            mongo_doc_type.objects.delete()

    @timeit
    def get_all(self, name_of_table):
        mongo_doc_type = self.collections.get(name_of_table)
        if not mongo_doc_type:
            return
        return list(mongo_doc_type.objects)

    def save(self, name_of_table, link, status=None):
        mongo_doc_type = self.collections.get(name_of_table)
        if not mongo_doc_type:
            return
        obj: mongo.Document = mongo_doc_type(url=link, status=status)
        if mongo_doc_type.objects(url=link).count() == 0:
            obj.save()

    def _save(self, collection_name, **kwargs):
        if not kwargs.get("url"):
            return
        mongo_doc_type = self.collections.get(collection_name)
        if not mongo_doc_type:
            return
        obj: mongo.Document = mongo_doc_type(**kwargs)
        s = time.time()
        desired_objects = mongo_doc_type.objects(url=kwargs["url"])
        print('QQQ:', time.time() - s)
        if desired_objects.count() == 0:
            obj.save()

    def create_db(self):
        pass

    def get_video_with_status(self, status):
        res = list(Video.objects(status=status))
        if not res:
            return ""
        else:
            return res[0].url

    def set_status(self, link, status):
        for video in Video.objects(link=link):
            video.status = status

    def get_videos_with_status(self, status):
        return list(Video.objects(status=status))


#
if __name__ == '__main__':
    from src.config import mongo_password, mongo_username
    parser = MongoParser(atlas=True,
                         username=mongo_username,
                         password=mongo_password)
    # parser = MongoParser()
    print('connected')
    # parser._save('video', url='http://base', status='done')
    # print([obj.url for obj in parser.get_all('video')])
    print(parser.get_all('video'))
#     mongo.connect('data0')
#     for ob in Video.objects:
#         print(ob)
#         print(type(ob))
#         print(ob.__init_subclas__())
#         break
