from src.processing.yt_upload.google_api_utils import Create_Service
import os


def get_abs_path(relative_path):
    dir_name = os.path.dirname(__file__)
    return os.path.join(dir_name, relative_path)


def add_video_to_playlist(video_id, playlist_id, app_version=4):
    CLIENT_SECRET_FILE = get_abs_path(f'client_secrets\client_secret_{app_version}.json')
    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
              'https://www.googleapis.com/auth/youtube']

    service = Create_Service(
        CLIENT_SECRET_FILE, API_NAME, API_VERSION, app_version, SCOPES
    )
    request_body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }

    service.playlistItems().insert(
        part="snippet",
        body=request_body,
    ).execute()
