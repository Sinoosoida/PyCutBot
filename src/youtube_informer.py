import requests
import bs4
from datetime import datetime
from typing import List


class YtVideo:
    def __init__(self, entry: bs4.element.Tag):
        self.video_id: str = entry.find("yt:videoid").contents[0]
        group: bs4.element.Tag = entry.find("media:group")
        self.watch_url: str = group.find("media:content")["url"]
        self.thumbnail_url: str = group.find("media:thumbnail")["url"]
        self.channel_id: str = entry.find("yt:channelid").contents[0]
        published_at_str: str = entry.find("published").contents[0]
        self.published_at: datetime = datetime.strptime(
            published_at_str.rsplit("+")[0], "%Y-%m-%dT%H:%M:%S"
        )

    def download_silent_video(self):
        pass

    def download_audio(self):
        pass


class YtPlaylist:
    def __init__(self, playlist_id: str):
        response = requests.get(f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}")
        if response.status_code != 200:
            raise ValueError("YT_INFO error: Invalid playlist")
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
        return [YtVideo(entry) for entry in self.__soup.find_all("entry")]

# playlist_id = 'PL4_hYwCyhAvZain8aQHEYJ9rj9pg7ojFf'
# response = requests.get(f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}")
# doc = response.content.decode('utf-8')
# soup = bs4.BeautifulSoup(doc, "lxml")
