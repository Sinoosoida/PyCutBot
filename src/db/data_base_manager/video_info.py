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

    def get_publish_time(self, video_id) -> datetime:
        res = self.service.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id,
        ).execute()

        dt_str = res['items'][0]['snippet']['publishedAt']
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%SZ')
