from pytube import Playlist
from pytube import YouTube
import sqlite3
import json
import requests
import os
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build


def find_best_resolution_stream(link):
    yt = YouTube(link)
    res = 0
    for i in yt.streams:
        if not (i.resolution is None):
            if int(i.resolution[0:-1]) > res:
                res = int(i.resolution[0:-1])
                stream = i
    return stream


def find_best_abr_stream(link):
    yt = YouTube(link)
    abr = 0
    for i in yt.streams:
        if not (i.abr is None) and (i.type == "audio"):
            if int(i.abr[0:-4]) > abr:
                abr = int(i.abr[0:-4])
                stream = i
    return stream


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
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()


def download_from_youtube(link):
    all_streams = YouTube(link).streams
    if len(all_streams.filter(only_audio=True)) == 0:
        video_path = all_streams.get_highest_resolution().download()
        return os.path.basename(video_path), None
    else:
        video_path = find_best_resolution_stream(link).download()
        stream = find_best_abr_stream(link)
        audio_path = stream.download()
        return os.path.basename(video_path), os.path.basename(audio_path)


def get_name(link):
    return YouTube(link).title


def good_link(link):
    if YouTube(link).length > (3600 * 3):
        return False
    return True


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
