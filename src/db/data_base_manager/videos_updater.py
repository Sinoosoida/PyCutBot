import time
from src.db.mongo_parser.mongo_parser import MongoParser
from src.db.mongo_parser.collections_schemas import Status
from src.config import mongo_password, mongo_username
from src.db.data_base_manager.updater_utils import *
from datetime import datetime, timedelta
from src.processing.yt_upload.add_to_playlist import add_video_to_playlist
from src.processing.yt_upload.create_playlist import create_playlist
from log import *
import sys
import requests as req
from concurrent.futures import ThreadPoolExecutor
import src.db.mongo_parser.collections_schemas as schema
from src.yt_informer import YtPlaylist

MAX_PLAYLISTS = None if len(sys.argv) == 1 else int(sys.argv[1])

parser = MongoParser(atlas=True,
                     username=mongo_username,
                     password=mongo_password)


def videos_from_channel():  # adding all new videos from the channel
    print_header1_info("Processing videos_from_channel")
    try:
        channel: schema.Channel
        for channel in parser.get_all("channel"):
            print_info(f"Processing {channel.channel_id} channel")
            try:
                last_request_time = channel.last_request_datetime
                start_processing_time = datetime.now()
                print('last_request_time', last_request_time)
                print('start_processing_time', start_processing_time)
                videos = get_videos_since_date(channel.channel_id, last_request_time - timedelta(minutes=10))
                for video in videos:
                    if parser.save(collection_name="video",
                                   url=video.watch_url,
                                   video_id=video.video_id,
                                   channel_id=video.channel_id,
                                   published_at=video.published_at,
                                   status="in queue"):
                        print_info(f"Adding video {video.video_id} to database")
                parser.set(collection_name="channel", channel_id=channel.channel_id,
                           last_request_datetime=start_processing_time)
                print_info(f"Last request time was updated {start_processing_time.time()} t")
                print_success(f"Processing {channel.channel_id} channel done")
            except Exception as ex:
                print_error("Impossible to process this channel", ex)
        print_success("Making videos from channels done")
    except Exception as exc:
        print_error("Fatal error. Impossible to make videos from channel.", exc)


def videos_from_playlists():  # all videos from the right playlists
    print_header1_info("Processing videos from playlists")
    try:
        playlist: schema.Playlist
        for playlist in parser.get_playlists_with_load_all():
            for video in YtPlaylist(playlist.playlist_id).videos:
                if parser.save(collection_name="video",
                               url=video.watch_url,
                               video_id=video.video_id,
                               channel_id=video.channel_id,
                               published_at=video.published_at,
                               status="in queue"):
                    print_info(f"Adding video {video.video_id} to database")
        print_success("Processing videos from playlists done")
    except Exception as ex:
        print_error("Fatal error. Impossible to make videos from playlists", ex)


def playlists_from_channel():
    print_header1_info("Processing playlists channel")
    try:
        channel: schema.Channel
        for channel in parser.get_all("channel"):
            for playlist_id in get_all_playlists_ids(channel.channel_id, max_res=MAX_PLAYLISTS):
                if parser.save('playlist', playlist_id=playlist_id, load_all=False):
                    print_info(f"Adding playlist {playlist_id} playlist to database")
        print_success("Processing playlists from channel done")
    except Exception as ex:
        print_error("Fatal error. Impossible to get playlists from channel.", ex)


def playlist_to_video():  # adding playlist links to video parameters
    print_header1_info("Adding playlists to video list")
    try:
        playlist: schema.Playlist
        for playlist in parser.get_all("playlist"):
            for video_url in YtPlaylist(playlist.playlist_id).videos:
                if parser.add_playlist_to_video(url=video_url, playlist_url=playlist.playlist_id):
                    print_info(f"Adding playlist {playlist.playlist_id} to {video_url} list")
        print_success("Adding playlists to video list done")
    except:
        print_error("Fatal error. Impossible to add playlists to video list.")


def load_videos_to_playlist():
    print_header1_info("Loading videos with 'done' status to playlist")
    try:
        for video in parser.get_all("video"):
            print(video)
            if video.status == Status.DONE:
                print("gonna add")
                playlist: schema.Playlist
                for playlist in parser.get_attr('video', video.url, attribute_name='playlists_urls'):
                    if not playlist.uploaded:
                        playlist_url = playlist.playlist_url
                        print_info(f"Adding video {video.url} to playlist {playlist_url} playlist")
                        try:
                            if not parser.get_attr('playlist', playlist["playlist_url"], 'new_playlist_id'):
                                print_info(f"Creating new playlist for {playlist_url}")
                                create_playlist(playlist_url)
                            add_video_to_playlist(video.new_video_id,
                                                  parser.get_attr('playlist', playlist_url, 'new_url'))
                            parser.mark_playlist_as_upload(video.url, playlist["playlist_url"])
                            print_success(f"Adding video {video.url} to playlist {playlist_url} done")
                        except:
                            print_error(f"Adding video {video.url} to playlist {playlist_url} error")

        print_success("Loading videos to playlists done")
    except:
        print_error("Fatal error. Impossible to load videos to playlists.")


def update_videos():
    videos_from_channel()
    playlists_from_channel()
    videos_from_playlists()
    playlist_to_video()
    load_videos_to_playlist()


sleep_time = 5 * 60


def main():
    while True:
        update_videos()
        print_sep()
        time.sleep(sleep_time)


def down_detector():
    while True:
        try:
            req.get(f'http://51.15.75.62:5000/upd?service=pycutbot_updater&time_delta={sleep_time}')
        except Exception as ex:
            print_error("DOWNDETECTOR EX", ex)
        time.sleep(sleep_time)


while True:
    with ThreadPoolExecutor() as executor:
        main_future = executor.submit(main)
        down_detector_future = executor.submit(down_detector)
