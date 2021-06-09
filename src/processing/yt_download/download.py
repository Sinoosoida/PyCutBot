import warnings
import os
from pytube import YouTube
import requests


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


def download_video(yt_obj, path="./"):
    return find_best_resolution_stream(yt_obj).download(output_path=path)


def download_audio(yt_obj, path="./"):
    return find_best_abr_stream(yt_obj).download(output_path=path)


def download_thumbnail(yt_object: YouTube, path="./"):
    url = yt_object.thumbnail_url
    full_path = os.path.abspath(os.path.join(path, 'thumbnail.png'))
    with open(full_path, 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            return None
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return full_path


def good_link(link):
    if YouTube(link).length > (3600 * 3):
        return False
    return True


def get_yt_object(link):
    return YouTube(link)


def download_video_from_youtube(yt_object: YouTube, video_dir, audio_dir, thumbnail_dir):
    video_name = yt_object.title
    print(video_name)
    video_path = download_video(yt_object, video_dir)
    print(os.path.abspath(video_path))
    audio_path = download_audio(yt_object, audio_dir)
    print(os.path.abspath(audio_path))
    thumbnail_path = download_thumbnail(yt_object, thumbnail_dir)
    print(thumbnail_path)
    if not audio_path:
        warnings.warn(message="have not audio", category=UserWarning, stacklevel=1)
    if not video_path:
        warnings.warn(message="have not audio", category=UserWarning, stacklevel=1)
    if not thumbnail_path:
        warnings.warn(message="have not thumbnail", category=UserWarning, stacklevel=1)
    print(str(video_path) + " " + str(audio_path))
    print("downloading done")

    return video_name, video_path, audio_path, thumbnail_path