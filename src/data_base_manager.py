from networking import *
from db import SQLParser


def videos_from_channel(data_base):
    for channel in data_base.get_all("channel"):
        for video in get_videos_from_channel(channel):
            data_base.save("video", video, "in queue")


def videos_from_playlists(data_base):
    for playlist in data_base.get_all("playlist"):
        for video in get_videos_from_playlist(playlist):
            data_base.save("video", video, "in queue")
