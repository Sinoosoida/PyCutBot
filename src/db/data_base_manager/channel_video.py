from datetime import datetime
from src.processing.yt_upload.google_api_utils import Create_Service
import os


def get_abs_path(relative_path):
    dir_name = os.path.dirname(__file__)
    return os.path.join(dir_name, relative_path)


class VideoInfoGetter:
    def __init__(self, app_version):
        CLIENT_SECRET_FILE = get_abs_path(f'..\..\google_api\client_secrets\client_secret_{app_version}.json')

        API_NAME = "youtube"
        API_VERSION = "v3"
        SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
                  'https://www.googleapis.com/auth/youtube.upload',
                  'https://www.googleapis.com/auth/youtube',
                  'https://www.googleapis.com/auth/youtube.readonly']

        self.service = Create_Service(
            CLIENT_SECRET_FILE, API_NAME, API_VERSION, app_version, SCOPES
        )

    def last_50_videos(self, channel_id):
        res = self.service.search().list(
            part="snippet,id",
            channelId=channel_id,
            order='date',
            maxResults=50
        ).execute()

        return [video['id']['videoId'] for video in res['items']]


v = VideoInfoGetter(5)
from pprint import pprint

pprint(v.last_50_videos('UCppkxNOs8rEuhEyk0GtrfRg'))
