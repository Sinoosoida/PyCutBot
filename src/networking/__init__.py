from pytube import YouTube
import os
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import warnings


def find_best_resolution_stream(yt_obj):
    res = 0
    best_resolution_stream = yt_obj.streams[0]
    for stream in yt_obj.streams[1:]:
        if stream.resolution and int(stream.resolution[0:-1]) > res:
            res = int(stream.resolution[0:-1])
            best_resolution_stream = stream
    return best_resolution_stream


def find_best_abr_stream(yt_obj):
    abr = 0
    best_abr_stream = yt_obj.streams[0]
    for stream in yt_obj.streams[1:]:
        if stream.abr and stream.type == "audio" and int(stream.abr[0:-4]) > abr:
            abr = int(stream.abr[0:-4])
            best_abr_stream = stream
    return best_abr_stream


def send_to_google_drive(file_path, name):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = './drive-keys.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    folder_id = '1n1Zi4KbOKQgOaoKyYuo4Vs0vARAhXsBr'
    file_metadata = {
        'name': name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()


#
#
# def download_from_youtube(link):
#     all_streams = YouTube(link).streams
#     if len(all_streams.filter(only_audio=True)) == 0:
#         video_path = all_streams.get_highest_resolution().download()
#         return os.path.basename(video_path), None
#     video_path = find_best_resolution_stream(link).download()
#     audio_path = find_best_abr_stream(link).download()
#     return os.path.basename(video_path), os.path.basename(audio_path)


def good_link(link):
    if YouTube(link).length > (3600 * 3):
        return False
    return True


def get_yt_object(link):
    return YouTube(link)


# def get_info(yt_obj: YouTube):
#     return {'title': yt_obj.title,
#             'description': yt_obj.description,
#             ''
#             'thumbnail_url': yt_obj.thumbnail_url
#             }


def download_video(yt_obj, path="./"):
    return find_best_resolution_stream(yt_obj).download(output_path=path)


def download_audio(yt_obj, path="./"):
    return find_best_abr_stream(yt_obj).download(output_path=path)


def download(link, video_dir, audio_dir):
    yt_object = YouTube(link)
    video_name = yt_object.title
    print(video_name)
    video_path = download_video(link, video_dir)
    print(video_path)
    audio_path = download_audio(link, audio_dir)
    print(video_path)
    if not audio_path:
        warnings.warn(message="have not audio", category=UserWarning, stacklevel=1)
    if not video_path:
        warnings.warn(message="have not audio", category=UserWarning, stacklevel=1)
    print(str(video_path) + " " + str(audio_path))
    print("downloading done")
    return video_name, video_path, audio_path, yt_object
