from src.requests_utils import get_request_with_retries
import json
import src.config as config
from pytube import Channel, Playlist, YouTube
from tqdm import tqdm
import datetime
from datetime import datetime, timedelta
from channel_video import get_last_video_urls
from video_info import VideoInfoGetter

from utils import timeit


def get_videos_url_from_channel(channel):
    return Channel(channel).video_urls


def get_videos_url_from_playlist(playlist):
    return Playlist(playlist).video_urls


@timeit
def get_channel_video_urls(channel):
    return list(channel.video_urls)


video_info_getter = VideoInfoGetter(app_version=5)


def get_videos_urls_since_date(channel_url, date=datetime.min):
    """
    По дефолту date - минимальная, т.е. если хочешь получить все видосы на канале, просто не указывай ее как аргумент
    :param channel_url:
    :param date:
    :return:
    """

    res = []
    channel = Channel(channel_url)
    urls = get_last_video_urls(channel.channel_id)
    for url in urls:
        video = YouTube(url)
        print(video.watch_url)
        publish_dt = video_info_getter.get_publish_time(video.video_id)
        print('published:', publish_dt)
        if publish_dt >= date:
            res.append(video.watch_url)
        else:
            return res

    return res


def channel_url_to_id(url):
    return Channel(url).channel_id


@timeit
def get_all_playlists(channel_url: str, key=config.api_key):
    playlists_list = []
    channel_id = channel_url_to_id(channel_url)
    res = get_request_with_retries(
        f'https://www.googleapis.com/youtube/v3/playlists?channelId={channel_id}&key={key}&maxResults=50')
    if not res:
        return playlists_list

    res_dict = json.loads(res.content)
    for dct in res_dict['items']:
        playlists_list.append('https://www.youtube.com/playlist?list=' + dct['id'])

    while res_dict.get('nextPageToken'):
        # print(res_dict.get('nextPageToken'))
        res = get_request_with_retries(
            f"https://www.googleapis.com/youtube/v3/playlists?channelId={channel_id}"
            f"&key={key}&maxResults=50&pageToken={res_dict.get('nextPageToken')}")
        if not res:
            return playlists_list
        res_dict = json.loads(res.content)
        for dct in res_dict['items']:
            playlists_list.append('https://www.youtube.com/playlist?list=' + dct['id'])
    return playlists_list


def update_playlists(parser):
    for channel in parser.get_all("channel"):
        for playlist_url in get_all_playlists(channel.url):
            parser.save('playlist', url=playlist_url, load_all=False)

#
# from pprint import pprint
#
# r = get_videos_urls_since_date('https://www.youtube.com/c/telesport', datetime.now() - timedelta(hours=1))
# pprint(r)

# v = VideoInfoGetter(5)
# print(v.get_publish_time('3p-IXhsFfnM'))

# utc_dt = local_dt.astimezone(pytz.utc)
#
# print(utc.localize(dt, is_dst=None))
