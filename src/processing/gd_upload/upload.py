from google.oauth2 import service_account
from google.protobuf import service
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
import pprint
import os

import google.oauth2
#import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io


def create_folder_on_google_drive(name=None, folder_id):#должен создавать папку на google drive и возвращать её id
    return folder_id

def upload_file_on_google_drive(name=None, folder_id):#должен создавать папку на google drive и возвращать её id
    return file_id

def upload_path(path, folder_id="1PGHW4Crd2PYZdhIZT8a69pG4Di7Q6gn7", new_name=None):
    filename, file_extension = os.path.splitext(path)
    if file_extension==None:#если это папка
        new_folder_id = create_folder_on_google_drive(new_name, folder_id)
        files = os.listdir(path)
        for file in files:
            upload_path(path+filse, new_folder_id, None)
        return new_folder_id
    else:
        upload_file_on_google_drive()
    print(filename)
    print(file_extension)
    files = os.listdir(path)


def upload_to_prod_google_drive(title, main_folder_id="1PGHW4Crd2PYZdhIZT8a69pG4Di7Q6gn7"):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = './google_drive_api.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    folder_id = main_folder_id
    file_metadata = {
        'name': name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()


def download_from_prod_google_drive(file_id):
    request = service.files().get_media(fileId=file_id)
    filename = '/home/makarov/File.csv'
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


def upload_to_pub_google_drive(title, main_floader_id="1PGHW4Crd2PYZdhIZT8a69pG4Di7Q6gn7"):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = './google_drive_api.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    folder_id = main_floader_id
    file_metadata = {
        'name': name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()


upload_dir("../media")
