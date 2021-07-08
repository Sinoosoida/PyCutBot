import mongoengine as mongo
from abc import abstractmethod, ABCMeta
from utils import Singleton
from enum import Enum, auto
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
    IN_QUEUE = 'in queue'
    DONE = 'done'
    ERROR = 'error'

    # extras:
    PROCESSING = 'processing'


class Video(mongo.Document):
    url = mongo.StringField(required=True)
    status = mongo.EnumField(Status, default=Status.IN_QUEUE)
    playlists_urls = mongo.ListField(mongo.StringField())


class Playlist(mongo.Document):
    url = mongo.StringField(required=True)


class Channel(mongo.Document):
    url = mongo.StringField(required=True)
    last_request_datetime = mongo.DateTimeField(default=datetime.min)


class MongoParser(metaclass=Singleton):
    def __init__(self, db_name='data0'):
        mongo.connect(db_name)
        self.collections = {'video': Video,
                            'playlist': Playlist,
                            'channel': Channel}

    def clear_db(self, name_of_table=None):
        if not name_of_table:
            print('no name_of_table specified, exiting')
            return
        print(self.get_all(name_of_table))
        if input('Are you sure? y/n') == 'y':
            mongo_doc_type = self.collections.get(name_of_table)
            if not mongo_doc_type:
                return
            mongo_doc_type.objects.delete()

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

    def __save(self, collection_name, **kwargs):
        if not kwargs.get('url'):
            return
        mongo_doc_type = self.collections.get(collection_name)
        if not mongo_doc_type:
            return
        obj: mongo.Document = mongo_doc_type(**kwargs)
        if mongo_doc_type.objects(url=kwargs['url']).count() == 0:
            obj.save()

    def create_db(self):
        pass

    def get_video_with_status(self, status):
        res = list(Video.objects(status=status))
        if not res:
            return ''
        else:
            return res[0].url

    def set_status(self, link, status):
        for video in Video.objects(link=link):
            video.status = status

    def get_videos_with_status(self, status):
        return list(Video.objects(status=status))

#
# if __name__ == '__main__':
#     parser = MongoParser()
#     mongo.connect('data0')
#     for ob in Video.objects:
#         print(ob)
#         print(type(ob))
#         print(ob.__init_subclas__())
#         break
