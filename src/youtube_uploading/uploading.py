import datetime
from src.youtube_uploading.google_api_utils import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = r"youtube_uploading/client_secret.json"
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def upload_video_to_youtube(video_path, thumbnail_path, title, description, tags):
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

    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload(thumbnail_path)
    ).execute()
