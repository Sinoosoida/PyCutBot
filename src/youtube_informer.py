import requests
import bs4
from datetime import datetime
from typing import List
import json


class YtVideo:
    def __init__(self, video_id: str, channel_id: str, published_at: datetime):
        self.video_id: str = video_id
        self.watch_url: str = "http://www.youtube.com/watch?v=" + video_id
        self.__query = f"https://www.youtube.com/oembed?url={self.watch_url}&format=json"
        if requests.get(self.__query).status_code != 200:
            raise ValueError("YT_INFO error: Invalid video id")
        self.channel_id = channel_id
        self.published_at = published_at

    @classmethod
    def from_entry(cls, entry: bs4.element.Tag):
        video_id: str = entry.find("yt:videoid").contents[0]
        channel_id: str = entry.find("yt:channelid").contents[0]
        published_at_str: str = entry.find("published").contents[0]
        published_at: datetime = datetime.strptime(
            published_at_str.rsplit("+")[0], "%Y-%m-%dT%H:%M:%S"
        )
        return cls(video_id, channel_id, published_at)

    @property
    def __json(self) -> dict:
        response = requests.get(self.__query)
        return json.loads(response.content.decode('utf-8'))

    @property
    def title(self) -> str:
        return self.__json.get('title')

    @property
    def author_name(self) -> str:
        return self.__json.get('author_name')

    @property
    def author_url(self) -> str:
        return self.__json.get('author_url')

    @property
    def thumbnail_url(self) -> str:
        return self.__json.get('thumbnail_url')

    def download_silent_video(self):
        pass

    def download_audio(self):
        pass

    def download_thumbnail(self):
        pass

    def __str__(self):
        return str(self.__dict__)


class YtPlaylist:
    def __init__(self, playlist_id: str):
        response = requests.get(f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}")
        if response.status_code != 200:
            raise ValueError("YT_INFO error: Invalid playlist id")
        self.playlist_id = playlist_id

    @property
    def __soup(self):
        response = requests.get(f"https://www.youtube.com/feeds/videos.xml?playlist_id={self.playlist_id}")
        doc = response.content.decode("utf-8")
        return bs4.BeautifulSoup(doc, "lxml")

    @property
    def title(self) -> str:
        return self.__soup.find("title").contents[0]  # todo: check if text exists

    @property
    def owner(self) -> str:
        return self.__soup.find("author").find("name").contents[0]

    @property
    def videos(self) -> List[YtVideo]:
        return [YtVideo.from_entry(entry) for entry in self.__soup.find_all("entry")]


# playlist_id = 'PL4_hYwCyhAvZain8aQHEYJ9rj9pg7ojFf'
# response = requests.get(f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}")
# doc = response.content.decode('utf-8')
# soup = bs4.BeautifulSoup(doc, "lxml")

YtVideo('xuCn8ux2gbs')
