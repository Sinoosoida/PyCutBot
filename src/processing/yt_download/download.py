import os

import requests
from pytube import YouTube

from src.processing.core.load_audio import webm2wav
from src.requests_utils import with_retries
from src.utils import fix_filename


def find_best_resolution_stream(yt_obj: YouTube):
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


@with_retries(3)
def download_video(yt_obj, path="./"):
    return find_best_resolution_stream(yt_obj).download(output_path=path)


@with_retries()
def download_audio(yt_obj, path="./"):
    return find_best_abr_stream(yt_obj).download(output_path=path)


@with_retries()
def download_thumbnail(yt_object: YouTube, path="./"):
    url = yt_object.thumbnail_url
    full_path = os.path.abspath(os.path.join(path, "thumbnail.png"))
    with open(full_path, "wb") as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            return None
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return full_path


@with_retries()
def good_link(link):
    return YouTube(link).length <= (3600 * 3)


@with_retries()
def get_yt_object(link) -> YouTube:
    return YouTube(link)


@with_retries(5)
def get_clear_name(yt_object):
    real_title: str = yt_object.title
    return real_title.replace(r'/', '|').replace('\\', '|').replace('.', '')


def download_video_from_youtube(yt_object: YouTube, video_dir, audio_dir, thumbnail_dir):
    video_name = "unknown"
    real_name = get_clear_name(yt_object)
    if real_name:
        video_name = real_name
    video_path = download_video(yt_object, video_dir)
    if not video_path:
        return False
    video_path = fix_filename(video_path)
    webm_audio_path = download_audio(yt_object, audio_dir)
    if not webm_audio_path:
        return False
    webm_audio_path = fix_filename(webm_audio_path)
    audio_path = webm2wav(video_path, webm_audio_path)
    thumbnail_path = download_thumbnail(yt_object, thumbnail_dir)
    if not thumbnail_path:
        return False  # todo
    thumbnail_path = fix_filename(thumbnail_path)

    return video_name, video_path, audio_path, thumbnail_path
