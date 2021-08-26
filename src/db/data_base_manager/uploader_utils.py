from src.requests_utils import get_request_with_retries
import json
import src.config as config
from tqdm import tqdm
import datetime
from datetime import datetime, timedelta
from channel_video import get_last_videos
from video_info import VideoInfoGetter
from typing import List
from src.db.data_base_manager.info import YtVideo, YtPlaylist

from utils import timeit

video_info_getter = VideoInfoGetter(app_version=5)


def get_videos_since_date(channel_id, date=datetime.min):
    """
    По дефолту date - минимальная, т.е. если хочешь получить все видосы на канале, просто не указывай ее как аргумент
    :param channel_id:
    :param date:
    :return:
    """

    res = []
    videos: List[YtVideo] = get_last_videos(channel_id)
    for video in videos:
        print(video.watch_url)
        publish_dt = video.published_at
        print('published:', publish_dt)
        if publish_dt >= date:
            res.append(video.watch_url)
        else:
            return res

    return res


def get_all_playlists(channel_id: str, key=config.api_key, max_res=None):
    playlists_list = []
    res = get_request_with_retries(
        f'https://www.googleapis.com/youtube/v3/playlists?channelId={channel_id}&key={key}&maxResults=50')
    if not res:
        return playlists_list

    res_dict = json.loads(res.content)
    for dct in res_dict['items']:
        playlists_list.append(dct['id'])

    num_res = 50

    def under_limit(num_res):
        return True if not max_res or max_res < num_res else False

    while res_dict.get('nextPageToken') and under_limit(num_res):
        # print(res_dict.get('nextPageToken'))
        res = get_request_with_retries(
            f"https://www.googleapis.com/youtube/v3/playlists?channelId={channel_id}"
            f"&key={key}&maxResults=50&pageToken={res_dict.get('nextPageToken')}")
        if not res:
            return playlists_list
        res_dict = json.loads(res.content)
        for dct in res_dict['items']:
            playlists_list.append(dct['id'])
    return playlists_list

# def update_playlists(parser):
#     for channel in parser.get_all("channel"):
#         for playlist_url in get_all_playlists(channel.url):
#             parser.save('playlist', url=playlist_url, load_all=False)

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
