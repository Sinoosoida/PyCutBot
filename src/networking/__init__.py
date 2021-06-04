from pytube import YouTube
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


def download_video(yt_obj, path="./"):
    return find_best_resolution_stream(yt_obj).download(output_path=path)


def download_audio(yt_obj, path="./"):
    return find_best_abr_stream(yt_obj).download(output_path=path)


def good_link(link):
    if YouTube(link).length > (3600 * 3):
        return False
    return True


<<<<<<< HEAD
def download_video(link, path="./"):
    yt = YouTube(link)
    res = 0
    for i in yt.streams:
        if not (i.resolution is None):
            if int(i.resolution[0:-1]) > res:
                res = int(i.resolution[0:-1])
                stream = i
    video_path = stream.download(output_path=path)
    return video_path


def download_audio(link, path="./"):
    yt = YouTube(link)
    abr = 0
    for i in yt.streams:
        if not (i.abr is None) and (i.type == "audio"):
            if int(i.abr[0:-4]) > abr:
                abr = int(i.abr[0:-4])
                stream = i
    audio_path = stream.download(output_path=path)
    return audio_path

def get_yt_object(link):
    return YouTube(link)


def download(yt_object, video_dir, audio_dir):
    video_name = yt_object.title
    print(video_name)
    video_path = download_video(yt_object, video_dir)
    print(video_path)
    audio_path = download_audio(yt_object, audio_dir)
    print(video_path)
    if not audio_path:
        warnings.warn(message="have not audio", category=UserWarning, stacklevel=1)
    if not video_path:
        warnings.warn(message="have not audio", category=UserWarning, stacklevel=1)
    print(str(video_path) + " " + str(audio_path))
    print("downloading done")
    return video_name, video_path, audio_path
>>>>>>> b27c84a158174f1a174d7fe3f0cb47dcb71f4de0
