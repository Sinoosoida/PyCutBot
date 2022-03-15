import json
from datetime import datetime
from channel_video import get_last_video_urls
from pytube import Channel, Playlist, YouTube
from video_info import VideoInfoGetter
import src.config as config
from src.requests_utils import get_request_with_retries


def get_videos_url_from_channel(channel):
    return Channel(channel).video_urls


def get_videos_url_from_playlist(playlist):
    return Playlist(playlist).video_urls


def get_channel_video_urls(channel):
    return list(channel.video_urls)


video_info_getter = VideoInfoGetter(app_version=5)


def get_videos_urls_since_date(channel_url, date=datetime.min):
    res = []
    channel = Channel(channel_url)
    urls = get_last_video_urls(channel.channel_id)
    for url in urls:
        video = YouTube(url)
        publish_dt = video_info_getter.get_publish_time(video.video_id)
        if publish_dt >= date:
            res.append(video.watch_url)
        else:
            return res

    return res


def channel_url_to_id(url):
    return Channel(url).channel_id


def get_all_playlists(channel_url: str, key=config.api_key, max_res=None):
    playlists_list = []
    channel_id = channel_url_to_id(channel_url)
    res = get_request_with_retries(
        f"https://www.googleapis.com/youtube/v3/playlists?channelId={channel_id}&key={key}&maxResults=50"
    )
    if not res:
        return playlists_list

    res_dict = json.loads(res.content)
    for dct in res_dict["items"]:
        playlists_list.append("https://www.youtube.com/playlist?list=" + dct["id"])

    num_res = 50

    def under_limit(num_res):
        return True if not max_res or max_res < num_res else False

    while res_dict.get("nextPageToken") and under_limit(num_res):
        res = get_request_with_retries(
            f"https://www.googleapis.com/youtube/v3/playlists?channelId={channel_id}"
            f"&key={key}&maxResults=50&pageToken={res_dict.get('nextPageToken')}"
        )
        if not res:
            return playlists_list
        res_dict = json.loads(res.content)
        for dct in res_dict["items"]:
            playlists_list.append("https://www.youtube.com/playlist?list=" + dct["id"])
    return playlists_list

