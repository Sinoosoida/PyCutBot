# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from src.db.data_base_manager.info import YtVideo
from typing import List


def get_last_videos(channel_id: str) -> List[YtVideo]:
    """
    returns last 15 video urls in reversed chronological order
    """
    response = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
    doc = response.content.decode('utf-8')
    soup = BeautifulSoup(doc, "lxml")
    return [YtVideo(entry) for entry in soup.find_all("entry")]
    # return [group.find("media:content")['url'] for group in soup.find_all("media:group")]

#
channel_id = 'UCdxesVp6Fs7wLpnp1XKkvZg'
response = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
doc = response.content.decode('utf-8')
soup = BeautifulSoup(doc, "lxml")
# print(channel_id)
# print()
for entry in soup.find_all("entry"):
    print(type(entry))
    video_obj = YtVideo(entry)
    print(video_obj.__dict__)
    # for group in soup.find_all("media:group"):
    #     print('watch url:', group.find("media:content")['url'])
    #     print('thumbnail url:', group.find("media:thumbnail")['url'])
    # e = entry.find("yt:videoid")
    # print('video id:', e.contents[0])
    # print(BeautifulSoup(e, "html"))
    # print(e.strip())
    print()
    exit()
# print(soup)
