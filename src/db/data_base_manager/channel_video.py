# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def get_last_video_urls(channel_id):
    """
    returns last 15 video urls in reversed chronological order
    """
    response = requests.get(
        f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    )
    doc = response.content.decode("utf-8")
    soup = BeautifulSoup(doc, "lxml")
    return [
        group.find("media:content")["url"] for group in soup.find_all("media:group")
    ]
