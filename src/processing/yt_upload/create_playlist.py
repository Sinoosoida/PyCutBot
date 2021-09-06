import os

from pytube import Playlist

from src.processing.yt_upload.google_api_utils import Create_Service


def get_abs_path(relative_path):
    dir_name = os.path.dirname(__file__)
    return os.path.join(dir_name, relative_path)


def create_playlist(old_playlist_url, app_version=5):
    playlist = Playlist(old_playlist_url)

    CLIENT_SECRET_FILE = get_abs_path(f"..\..\google_api\client_secrets\client_secret_{app_version}.json")
    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    # 'https://www.googleapis.com/auth/youtube.upload',
    #       'https://www.googleapis.com/auth/youtube']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, app_version, SCOPES)
    request_body = {
        "snippet": {
            "title": playlist.title,
            "description": f"Плейлист с канала {playlist.owner}, оригинал: {old_playlist_url}",
        }
    }

    playlist_info = (
        service.playlists()
        .insert(
            part="snippet",
            body=request_body,
        )
        .execute()
    )
    return playlist_info["id"]


# if __name__ == "__main__":
#     r = create_playlist('https://www.youtube.com/playlist?list=PLdLtk23ZM3V7HPXdvZj4dEYntgMFOwIr2')
#     print(r)
