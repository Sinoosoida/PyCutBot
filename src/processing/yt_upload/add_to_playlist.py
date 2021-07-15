from src.processing.yt_upload.google_api_utils import Create_Service
import os


def get_abs_path(relative_path):
    dir_name = os.path.dirname(__file__)
    return os.path.join(dir_name, relative_path)


def service_add_video_to_playlist(service, video_id, playlist_id):
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


def detached_add_video_to_playlist(video_id, playlist_id, app_version=4):
    CLIENT_SECRET_FILE = get_abs_path(relative_path=f'..\..\google_api\client_secrets\client_secret_{app_version}.json')
    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ['https://www.googleapis.com/auth/youtube']
    SCOPES = ["https://www.googleapis.com/auth/youtube"
    ]
    service = Create_Service(
        CLIENT_SECRET_FILE, API_NAME, API_VERSION, app_version, SCOPES
    )

    service_add_video_to_playlist(service, video_id, playlist_id)


detached_add_video_to_playlist('cIuYFCAJ2a8',
                               'PL9g0wNoD6byzUat1xHdcD2al-Cf_O7BDG')
