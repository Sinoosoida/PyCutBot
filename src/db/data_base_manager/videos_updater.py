from pytube import *
import datetime
from src.requests_utils import get_request_with_retries
import json
import src.config as config
from src.db.mongo_parser import Status, MongoParser, Collection
from datetime import datetime
from src.config import mongo_password, mongo_username


def get_videos_urls_since_date(channel_url, date=datetime.datetime.min):
    """
    По дефолту date - минимальная, т.е. если хочешь получить все видосы на канале, просто не указывай ее как аргумент
    :param channel_url:
    :param date:
    :return:
    """
    channel = Channel(channel_url)
    res = []
    for url in channel.video_urls:
        video = YouTube(url)
        print(type(video.publish_date))
        if video.publish_date >= date:
            res.append(url)
        else:
            return res
    return res


def get_all_playlists(channel_url: str, key=config.api_key):
    playlists_list = []
    channel_id = channel_url.rsplit('/channel/')[1]
    res = get_request_with_retries(
        f'https://www.googleapis.com/youtube/v3/playlists?channelId={channel_id}&key={key}&maxResults=50')
    if not res:
        return playlists_list

    res_dict = json.loads(res.content)
    for dct in res_dict['items']:
        playlists_list.append('https://www.youtube.com/playlist?list=' + dct['id'])

    while res_dict.get('nextPageToken'):
        print(res_dict.get('nextPageToken'))
        res = get_request_with_retries(
            f"https://www.googleapis.com/youtube/v3/playlists?channelId={channel_id}"
            f"&key={key}&maxResults=50&pageToken={res_dict.get('nextPageToken')}")
        if not res:
            return playlists_list
        res_dict = json.loads(res.content)
        for dct in res_dict['items']:
            playlists_list.append('https://www.youtube.com/playlist?list=' + dct['id'])
    return playlists_list


def get_videos_url_from_channel(channel):
    return Channel(channel).video_urls


def get_videos_url_from_playlist(playlist):
    return Playlist(playlist).video_urls


def videos_from_channel(parser):#done
    for channel in parser.get_all("channel"):
        last_request_time = channel.last_request_datetime
        parser.set(collection_name = "channel", url = channel.url, last_request_datetime=datetime.now())
        for video_url in get_videos_urls_since_date(channel.url, last_request_time):
            parser.save(collection_name="video", url=video_url, status="in queue")


def videos_from_playlists(parser):#done
    for playlist in parser.get_all("playlist"):
        for video_url in get_videos_url_from_playlist(playlist.url):
            parser.save(collection_name="video", url=video_url, status="in queue")
            parser.add_playlist_to_video(video_url, playlist.url)

def playlists_from_channel(parser):
    for channel in parser.get_all("channel"):
        for video_url in get_all_playlists(channel.url)
            parser.save(collection_name="playlist", url=video_url)


def update_videos(data_base):#    playlists_from_channel(parser)
    parser = MongoParser(atlas=True,
                         username=mongo_username,
                         password=mongo_password)
    playlists_from_channel(parser)
    videos_from_channel(parser)
    videos_from_playlists(parser)#обязатльно последний
