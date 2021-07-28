from src.db.mongo_parser.mongo_parser import MongoParser
from src.db.mongo_parser.collections_schemas import Status, Collection
from src.config import mongo_password, mongo_username
from src.db.data_base_manager.uploader_utils import *
from datetime import datetime
from src.processing.yt_upload.add_to_playlist import add_video_to_playlist
from src.processing.yt_upload.create_playlist import create_playlist


def videos_from_channel(parser):  # adding all new videos from the channel
    for channel in parser.get_all("channel"):
        last_request_time = channel.last_request_datetime
        parser.set(collection_name="channel", url=channel.url, last_request_datetime=datetime.now())
        videos_url = get_videos_urls_since_date(channel.url, last_request_time)
        for video_url in videos_url:
            parser.save(collection_name="video", url=video_url, status="in queue")


def videos_from_playlists(parser):  # all videos from the right playlists
    for playlist in parser.get_all("playlist"):
        if (playlist.load_all):
            for video_url in get_videos_url_from_playlist(playlist.url):
                parser.save(collection_name="video", url=video_url, status="in queue")
                parser.add_playlist_to_video(video_url, playlist.url)


def playlists_from_channel(parser):
    for channel in parser.get_all("channel"):
        for playlist_url in get_all_playlists(channel.url):
            parser.save('playlist', url=playlist_url, load_all=False)


def playlist_to_video(parser):  # adding playlist links to video parameters
    for playlist in parser.get_all("playlist"):
        # print(playlist)
        try:
            for video_url in get_videos_url_from_playlist(playlist.url):
                try:
                    parser.add_playlist_to_video(video_url, playlist.url)
                except:
                    print("error")
        except:
            print("error")


def load_videos_to_playlist(parser):
    for video in parser.get_all("video"):
        if (video.status == Status.DONE):
            for playlist in parser.get_attr('video', video.url, attribute_name='playlists_urls'):
                if (not playlist['uploaded']):
                    if (not parser.get_attr('playlist', playlist["playlist_url"], 'new_url')):
                        create_playlist(playlist["playlist_url"])
                    add_video_to_playlist(video.new_video_id,
                                          parser.get_attr('playlist', playlist["playlist_url"], 'new_url'))
                    parser.mark_playlist_as_upload(video.url, playlist["playlist_url"])


def update_videos(parser):
    videos_from_channel(parser)
    playlists_from_channel(parser)
    videos_from_playlists(parser)
    playlist_to_video(parser)
    load_videos_to_playlist(parser)


parser = MongoParser(atlas=True,
                     username=mongo_username,
                     password=mongo_password)

while (True):
    update_videos(parser)
