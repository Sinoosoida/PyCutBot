import mongoengine as mongo
from utils import Singleton, timeit
import src.db.mongo_parser.collections_schemas as schema
from log import print_success


class MongoParser(metaclass=Singleton):
    def __init__(self, db_name='data0', atlas=False, username=None, password=None):
        if atlas:
            host = (
                f"mongodb+srv://{username}:{password}"
                f"@cluster0.nhitr.mongodb.net/myFirst"
                f"Database?retryWrites=true&w=majority"
            )
            mongo.connect(host=host, db=db_name)
            print_success("connected to mongo atlas")
        else:
            mongo.connect(db=db_name)
        self.collections = {
            schema.Collection.VIDEO: schema.Video,
            schema.Collection.PLAYLIST: schema.Playlist,
            schema.Collection.CHANNEL: schema.Channel,
        }

    def _get_doc_type(self, collection_name):
        return self.collections.get(schema.Collection(collection_name))

    def get_all(self, collection_name) -> list:
        mongo_doc_type = self._get_doc_type(collection_name)
        if not mongo_doc_type:
            return []
        return list(mongo_doc_type.objects)

    def save(self, collection_name, **kwargs):
        if not kwargs.get("url"):
            return False
        mongo_doc_type = self._get_doc_type(collection_name)
        if not mongo_doc_type:
            return False
        new_doc: mongo.Document = mongo_doc_type(**kwargs)
        same_docs = mongo_doc_type.objects(url=kwargs["url"])
        if same_docs.count() == 0:
            new_doc.save()
            return True
        return False

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
        videos_list = schema.Video.objects(url__iexact=url)
        if not videos_list:
            return False
        video = videos_list[0]
        playlists_urls = []
        for playlist in video.playlists_urls:
            playlists_urls.append(playlist['playlist_url'])
        if playlist_url not in playlists_urls:
            video.playlists_urls.append(
                schema.PlaylistDict(playlist_url=playlist_url,
                                    uploaded=False)
            )
            video.save()
            return True
        return False

    @staticmethod
    @timeit
    def get_videos_with_status(status) -> list:
        return list(schema.Video.objects(status=schema.Status(status)))

    @staticmethod
    def get_video_with_status(status) -> schema.Video:
        res = MongoParser.get_videos_with_status(status)
        if res:
            return res[0]

    @staticmethod
    def mark_playlist_as_upload(url, playlist_url):
        # videos_list = schema.Video.objects(url__iexact=url)
        videos_list = schema.Video.objects(url__iexact=url)
        if not videos_list:
            return
        video = videos_list[0]

        for idx, pl_url in enumerate(video.playlists_urls):
            if pl_url.playlist_url == playlist_url:
                video.playlists_urls[idx].uploaded = True
                video.save()
                break

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


# if __name__ == '__main__':
#     from pprint import pprint
#     p = MongoParser('data1')
#     # p.save('video', url='url2', status='in queue')
#     # p.add_playlist_to_video(url='url2', playlist_url='playlist3')
#     p.mark_playlist_as_upload(url='url1', playlist_url='playlist2')
#     playlists = (p.get_attr('video', url='url1', attribute_name='playlists_urls'))
#     for pl in playlists:
#         print(pl.playlist_url, pl.uploaded)
