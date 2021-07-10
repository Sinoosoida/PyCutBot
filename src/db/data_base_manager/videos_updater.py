from src.db.mongo_parser import Status, MongoParser, Collection
from datetime import datetime
from src.config import mongo_password, mongo_username
from src.db.data_base_manager.uploader_utils import *


def videos_from_channel(parser):  # done
    for channel in parser.get_all("channel"):
        last_request_time = channel.last_request_datetime
        parser.set(collection_name="channel", url=channel.url, last_request_datetime=datetime.now())
        for video_url in tqdm(get_videos_urls_since_date(channel.url, last_request_time)):
            parser.save(collection_name="video", url=video_url, status="in queue")


def videos_from_playlists(parser):  # done
    for playlist in parser.get_all("playlist"):
        for video_url in get_videos_url_from_playlist(playlist.url):
            parser.save(collection_name="video", url=video_url, status="in queue")
            parser.add_playlist_to_video(video_url, playlist.url)


def playlists_from_channel(parser):
    for channel in parser.get_all("channel"):
        for playlist_url in tqdm(get_all_playlists(channel.url)):
            for video_url in get_videos_url_from_playlist(playlist_url):
                parser.add_playlist_to_video(video_url, playlist_url)


def update_videos(parser):  # playlists_from_channel(parser)
    # videos_from_channel(parser)
    # videos_from_playlists(parser)
    playlists_from_channel(parser)


def update_playlists(parser):
    for channel in parser.get_all("channel"):
        for playlist_url in get_all_playlists(channel.url):
            parser.save('playlist', url=playlist_url, load_all=False)


parser = MongoParser(atlas=True,
                     username=mongo_username,
                     password=mongo_password)
update_videos(parser)
