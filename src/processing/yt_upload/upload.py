import datetime
import os.path

from googleapiclient.http import MediaFileUpload

from src.processing.yt_upload.google_api_utils import Create_Service
from src.requests_utils import with_retries


def get_abs_path(relative_path):
    dir_name = os.path.dirname(__file__)
    return os.path.join(dir_name, relative_path)


def upload_video_to_youtube(video_path, title, description, tags, thumbnail_path=None, app_version=5) -> str:
    CLIENT_SECRET_FILE = get_abs_path(f"..\..\google_api\client_secrets\client_secret_{app_version}.json")
    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, app_version, SCOPES)
    upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + ".000Z"

    request_body = {
        "snippet": {
            "categoryI": 27,  # education
            "title": title,
            "description": description,
            "tags": tags,
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": upload_date_time,
            "selfDeclaredMadeForKids": False,
        },
        "notifySubscribers": False,
    }

    mediaFile = MediaFileUpload(video_path)

    response_upload = service.videos().insert(part="snippet,status", body=request_body, media_body=mediaFile).execute()

    new_video_id = response_upload.get("id")

    if not thumbnail_path:
        return new_video_id

    service.thumbnails().set(videoId=new_video_id, media_body=MediaFileUpload(thumbnail_path)).execute()

    return new_video_id


# if __name__ == "__main__":
#     upload_video_to_youtube(
#         video_path=r"C:\Users\79161\PycharmProjects\PyCutBot\media\output_video\test video.mp4",
#         thumbnail_path=None,
#         title="ttl",
#         description="d",
#         tags=[],
#     )
