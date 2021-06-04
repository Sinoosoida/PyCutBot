from pytube import *


def get_videos_from_channel(channel):
    return Channel(channel).video_urls


def get_videos_from_playlist(playlist):
    return Playlist(playlist).video_urls


def videos_from_channel(data_base):
    for channel in data_base.get_all("channel"):
        for video in get_videos_from_channel(channel[0]):
            data_base.save("video", video, "in queue")


def videos_from_playlists(data_base):
    for playlist in data_base.get_all("playlist"):
        for video in get_videos_from_playlist(playlist[0]):
            data_base.save("video", video, "in queue")


def update_videos(data_base):
    videos_from_playlists(data_base)
    videos_from_channel(data_base)
