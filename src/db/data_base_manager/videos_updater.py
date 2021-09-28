import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import requests as req
from pytube import Playlist

import src.db.mongo_parser.collections_schemas as schema
from log import *
from src.config import mongo_password, mongo_username
from src.db.data_base_manager.uploader_utils import *
from src.db.mongo_parser.collections_schemas import Collection, Status
from src.db.mongo_parser.mongo_parser import MongoParser
from src.processing.yt_upload.add_to_playlist import add_video_to_playlist
from src.processing.yt_upload.create_playlist import create_playlist

MAX_PLAYLISTS = None if len(sys.argv) == 1 else int(sys.argv[1])

from telegram import Bot

# костыль, да

bot = Bot(token='739844988:AAHEHt8KiT9czNUFJuvqXUgfJOOzDVGnJ70')  # @Geneticist_bot


def send_error(text):
    for chat_id in [496233529, 423216896]:
        try:
            bot.send_message(chat_id=chat_id, text=text)
        except Exception as ex:
            print(ex)


def videos_from_channel(parser: MongoParser):  # adding all new videos from the channel
    print_header1_info("Processing videos_from_channel")
    try:
        for channel in parser.get_all("channel"):
            print_info(f"Processing {channel.url} channel")
            try:
                last_request_time = channel.last_request_datetime
                start_processing_time = datetime.now()
                print("last_request_time", last_request_time)
                print("start_processing_time", start_processing_time)
                videos_url = get_videos_urls_since_date(channel.url, last_request_time - timedelta(minutes=10))
                for video_url in videos_url:
                    if parser.save(collection_name="video", url=video_url, status="in queue"):
                        print_info(f"Adding video {video_url} to database")
                parser.set(
                    collection_name="channel",
                    url=channel.url,
                    last_request_datetime=start_processing_time,
                )
                print_info(f"Last request time was updated {start_processing_time.time()} t")
                print_success(f"Processing {channel.url} channel done")
            except Exception:
                print_error("Impossible to process this channel")
                traceback.print_exc()
                send_error(str(traceback.format_exc()))
        print_success("Making videos from channels done")
    except Exception:
        print_error("Fatal error. Impossible to make videos from channel.")
        traceback.print_exc()
        send_error(str(traceback.format_exc()))


def videos_from_playlists(parser: MongoParser):  # all videos from the right playlists
    print_header1_info("Processing videos from playlists")
    try:
        for playlist in parser.get_playlists_with_load_all():
            for video_url in get_videos_url_from_playlist(playlist.url):
                if parser.save(collection_name="video", url=video_url, status="in queue"):
                    print_info(f"Adding video {video_url} to database")
                parser.add_playlist_to_video(video_url, playlist.url)
        print_success("Processing videos from playlists done")
    except Exception:
        print_error("Fatal error. Impossible to make videos from playlists")
        traceback.print_exc()
        send_error(str(traceback.format_exc()))


def playlists_from_channel(parser: MongoParser):
    print_header1_info("Processing playlists channel")
    try:
        for channel in parser.get_all("channel"):
            for playlist_url in get_all_playlists(channel.url, max_res=MAX_PLAYLISTS):
                if parser.save("playlist", url=playlist_url, load_all=False):
                    print_info(f"Adding playlist {playlist_url} to database")
        print_success("Processing playlists from channel done")
    except Exception:
        print_error("Fatal error. Impossible to get playlists from channel.")
        traceback.print_exc()
        send_error(str(traceback.format_exc()))


def playlist_to_video(parser: MongoParser):  # adding playlist links to video parameters
    print_header1_info("Adding playlists to video list")
    try:
        for playlist in tqdm(parser.get_all("playlist")):
            for video_url in get_videos_url_from_playlist(playlist.url):
                if "www" in video_url:  # super bad thing, will be replaced in youtube-dl branch later
                    video_url = video_url.replace("www.", "")
                if parser.add_playlist_to_video(video_url, playlist.url):
                    print_info(f"Adding playlist {playlist.url} to {video_url} list")
        print_success("Adding playlists to video list done")
    except Exception:
        print_error("Fatal error. Impossible to add playlists to video list.")
        traceback.print_exc()
        send_error(str(traceback.format_exc()))


def load_videos_to_playlist(parser: MongoParser):
    print_header1_info("Loading videos with 'done' status to playlist")
    try:
        for video in parser.get_videos_with_status(Status.DONE):
            for playlist in parser.get_attr("video", video.url, attribute_name="playlists_urls"):
                if not playlist.uploaded:
                    playlist_url = playlist.url
                    print_info(f"Adding video {video.url} to playlist {playlist_url} playlist")
                    try:
                        if not parser.get_attr("playlist", playlist["playlist_url"], "new_playlist_id"):
                            print_info(f"Creating new playlist for {playlist_url}")
                            new_playlist_id = create_playlist(playlist_url)
                            parser.set(
                                collection_name="playlist",
                                url=playlist_url,
                                new_playlist_id=new_playlist_id,
                            )
                        add_video_to_playlist(
                            video_id=video.new_video_id,
                            playlist_id=parser.get_attr("playlist", playlist_url, "new_playlist_id"),
                        )
                        parser.mark_playlist_as_upload(video.url, playlist["playlist_url"])
                        print_success(f"Adding video {video.url} to playlist {playlist_url} done")
                    except Exception:
                        print_error(f"Adding video {video.url} to playlist {playlist_url} error")
                        traceback.print_exc()
                        send_error(str(traceback.format_exc()))

        print_success("Loading videos to playlists done")
    except Exception:
        print_error("Fatal error. Impossible to load videos to playlists.")
        traceback.print_exc()
        send_error(str(traceback.format_exc()))


def update_videos(parser):
    videos_from_channel(parser)
    playlists_from_channel(parser)
    videos_from_playlists(parser)
    playlist_to_video(parser)
    load_videos_to_playlist(parser)


parser = MongoParser(atlas=True, username=mongo_username, password=mongo_password)

sleep_time = 5 * 60


def main():
    while True:
        if os.path.isfile("stop"):
            sys.exit()
        update_videos(parser)
        print_sep()
        time.sleep(sleep_time)


def down_detector():
    while True:
        try:
            req.get(f"http://51.15.75.62:5000/upd?service=pycutbot_updater&time_delta={sleep_time}")
        except Exception as ex:
            print_error("DOWNDETECTOR EX", ex)
        time.sleep(sleep_time)


while True:
    with ThreadPoolExecutor() as executor:
        main_future = executor.submit(main)
        down_detector_future = executor.submit(down_detector)
