import time

from src.db.mongo_parser.mongo_parser import MongoParser
from src.db.mongo_parser.collections_schemas import Status, Collection
from src.config import mongo_password, mongo_username
from src.db.data_base_manager.uploader_utils import *
from datetime import datetime, timedelta
from src.processing.yt_upload.add_to_playlist import add_video_to_playlist
from src.processing.yt_upload.create_playlist import create_playlist
from log import *
import sys
import requests as req
from concurrent.futures import ThreadPoolExecutor

MAX_PLAYLISTS = None if len(sys.argv) == 1 else int(sys.argv[1])


def videos_from_channel(parser):  # adding all new videos from the channel
    print_header1_info("Processing videos_from_channel")
    try:
        for channel in parser.get_all("channel"):
            print_info(f"Processing {channel.url} channel")
            try:
                last_request_time = channel.last_request_datetime
                start_processing_time = datetime.now()
                print('last_request_time', last_request_time)
                print('start_processing_time', start_processing_time)
                videos_url = get_videos_urls_since_date(channel.url, last_request_time - timedelta(minutes=10))
                for video_url in videos_url:
                    if parser.save(collection_name="video", url=video_url, status="in queue"):
                        print_info(f"Adding video {video_url} to database")
                parser.set(collection_name="channel", url=channel.url, last_request_datetime=start_processing_time)
                print_info(f"Last request time was updated {start_processing_time.time()} t")
                print_success(f"Processing {channel.url} channel done")
            except Exception as ex:
                print_error("Impossible to process this channel", ex)
        print_success("Making videos from channels done")
    except Exception as exc:
        print_error("Fatal error. Impossible to make videos from channel.", exc)


def videos_from_playlists(parser):  # all videos from the right playlists
    print_header1_info("Processing videos from playlists")
    try:
        for playlist in parser.get_all("playlist"):
            if (playlist.load_all):
                for video_url in get_videos_url_from_playlist(playlist.url):
                    if parser.save(collection_name="video", url=video_url, status="in queue"):
                        print_info(f"Adding video {video_url} to database")
                    parser.add_playlist_to_video(video_url, playlist.url)
        print_success("Processing videos from playlists done")
    except Exception as ex:
        print_error("Fatal error. Impossible to make videos from playlists", ex)


def playlists_from_channel(parser):
    print_header1_info("Processing playlists channel")
    try:
        for channel in parser.get_all("channel"):
            for playlist_url in get_all_playlists(channel.url, max_res=MAX_PLAYLISTS):
                if parser.save('playlist', url=playlist_url, load_all=False):
                    print_info(f"Adding playlist {playlist_url} to database")
        print_success("Processing playlists from channel done")
    except Exception as ex:
        print_error("Fatal error. Impossible to get playlists from channel.", ex)


def playlist_to_video(parser):  # adding playlist links to video parameters
    print_header1_info("Adding playlists to video list")
    try:
        for playlist in parser.get_all("playlist"):
            for video_url in get_videos_url_from_playlist(playlist.url):
                if parser.add_playlist_to_video(video_url, playlist.url):
                    print_info(f"Adding playlist {playlist.url} to {video_url} list")
        print_success("Adding playlists to video list done")
    except:
        print_error("Fatal error. Impossible to add playlists to video list.")


def load_videos_to_playlist(parser):
    print_header1_info("Loading videos with 'done' status to playlist")
    try:
        for video in parser.get_all("video"):
            if (video.status == Status.DONE):
                for playlist in parser.get_attr('video', video.url, attribute_name='playlists_urls'):
                    if not playlist.uploaded:
                        playlist_url = playlist.playlist_url
                        print_info(f"Adding video {video.url} to playlist {playlist_url} playlist")
                        try:
                            if not parser.get_attr('playlist', playlist["playlist_url"], 'new_url'):
                                print_info(f"Creating new playlist for {playlist_url}")
                                create_playlist(playlist_url)
                            add_video_to_playlist(video.new_video_id,
                                                  parser.get_attr('playlist', playlist["playlist_url"], 'new_url'))
                            parser.mark_playlist_as_upload(video.url, playlist["playlist_url"])
                            print_success(f"Adding video {video.url} to playlist {playlist_url} done")
                        except:
                            print_error(f"Adding video {video.url} to playlist {playlist_url} error")

        print_success("Loading videos to playlists done")
    except:
        print_error("Fatal error. Impossible to load videos to playlists.")


def update_videos(parser):
    videos_from_channel(parser)
    playlists_from_channel(parser)
    videos_from_playlists(parser)
    playlist_to_video(parser)
    load_videos_to_playlist(parser)


parser = MongoParser(atlas=True,
                     username=mongo_username,
                     password=mongo_password)

sleep_time = 5 * 60


def main():
    while True:
        update_videos(parser)
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
