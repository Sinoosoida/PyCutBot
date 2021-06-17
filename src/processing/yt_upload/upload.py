import datetime
import os.path
from googleapiclient.http import MediaFileUpload
from src.processing.yt_upload.google_api_utils import Create_Service
from src.requests_utils import with_retries


def get_abs_path(relative_path):
    dir_name = os.path.dirname(__file__)
    return os.path.join(dir_name, relative_path)


@with_retries(3)
def upload_video_to_youtube(video_path, title, description, tags,
                            thumbnail_path=None, app_version=4):
    CLIENT_SECRET_FILE = get_abs_path('client_secrets/client_secret_{app_version}.json')
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, app_version, SCOPES)
    upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'

    request_body = {
        'snippet': {
            'categoryI': 27,  # education
            'title': title,
            'description': description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload(video_path)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    if not thumbnail_path:
        return

    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload(thumbnail_path)
    ).execute()
