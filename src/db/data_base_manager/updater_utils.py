from src.requests_utils import get_request_with_retries
import json
import src.config as config
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from src.yt_informer import YtVideo
from typing import List


def get_last_videos(channel_id: str) -> List[YtVideo]:
    """
    returns last 15 video urls in reversed chronological order
    """
    response = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
    doc = response.content.decode('utf-8')
    soup = BeautifulSoup(doc, "lxml")
    return [YtVideo.from_entry(entry) for entry in soup.find_all("entry")]


def get_videos_since_date(channel_id: str, date: datetime = datetime.min) -> List[YtVideo]:
    res = []
    videos: List[YtVideo] = get_last_videos(channel_id)
    for video in videos:
        if video.published_at >= date:
            res.append(video)
        else:
            return res

    return res


def get_all_playlists_ids(channel_id: str, key=config.api_key, max_res=None) -> List[str]:
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
        res = get_request_with_retries(
            f"https://www.googleapis.com/youtube/v3/playlists?channelId={channel_id}"
            f"&key={key}&maxResults=50&pageToken={res_dict.get('nextPageToken')}")
        if not res:
            return playlists_list
        res_dict = json.loads(res.content)
        for dct in res_dict['items']:
            playlists_list.append(dct['id'])
    return playlists_list
