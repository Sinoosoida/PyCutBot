import io
import os
import shutil
from src.processing.dirs import *
import google.oauth2
from google.protobuf import service
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import io
import httplib2
import os

from apiclient import discovery
type_of_archive = "zip"
CHUNKSIZE = 1024*512

def pack_files():
    if os.path.exists(DIR_OF_UNPACKED_FILES + NAME_OF_UNZIPED_FILES):
        if os.path.exists(ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive):
            os.remove(ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive)
        shutil.make_archive(
            ZIP_FILE_DIR + ZIP_FILE_NAME, type_of_archive, DIR_OF_UNPACKED_FILES, NAME_OF_UNZIPED_FILES
        )
        # shutil.rmtree(DIR_OF_UNPACKED_FILES+name_of_unziped_files, ignore_errors=False, onerror=None)


def unpack_files():
    if os.path.exists(ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive):
        if os.path.exists(DIR_OF_UNPACKED_FILES + NAME_OF_UNZIPED_FILES):
            shutil.rmtree(DIR_OF_UNPACKED_FILES + NAME_OF_UNZIPED_FILES, ignore_errors=False, onerror=None)
        shutil.unpack_archive(
            ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive, DIR_OF_UNPACKED_FILES, type_of_archive
        )
        # os.remove(ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive)


def upload_to_pub_google_drive(video_path, title, main_folder_id="1PGHW4Crd2PYZdhIZT8a69pG4Di7Q6gn7"):
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_KEY_PATH, scopes=SCOPES)
    service = build("drive", "v3", credentials=credentials)
    file_metadata = {"name": title, "parents": [main_folder_id]}
    media = MediaFileUpload(video_path, chunksize=CHUNKSIZE, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return r


def download_from_prod_google_drive(file_id, file_path=ZIP_FILE_DIR, file_name=ZIP_FILE_NAME + "." + type_of_archive):
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_KEY_PATH, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_path + file_name, "wb")
    MediaIoBaseDownload()
    downloader = MediaIoBaseDownload(fh, request, chunksize=CHUNKSIZE)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    unpack_files()


def upload_to_prod_google_drive(title, main_folder_id="1PGHW4Crd2PYZdhIZT8a69pG4Di7Q6gn7"):
    pack_files()
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_KEY_PATH, scopes=SCOPES)
    service = build("drive", "v3", credentials=credentials)
    file_metadata = {"name": title, "parents": [main_folder_id]}
    media = MediaFileUpload(ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive, chunksize=CHUNKSIZE,resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return r