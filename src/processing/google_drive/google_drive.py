import io
import os
import shutil

import google.oauth2
import httplib2
from apiclient import discovery
from google.oauth2 import service_account
from google.protobuf import service
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from log import *
from src.processing.dirs import *

type_of_archive = "zip"
CHUNKSIZE = 1024 * 512
tech_google_drive_id = "1PGHW4Crd2PYZdhIZT8a69pG4Di7Q6gn7"
prod_google_grive_id = "1AG4XCwaIRHNacZzk6Nke9NnyD7mxe9Fe"


def pack_files():
    print_info("Packing files")
    if os.path.exists(DIR_OF_UNPACKED_FILES + NAME_OF_UNZIPED_FILES):
        if os.path.exists(ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive):
            os.remove(ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive)
        shutil.make_archive(
            ZIP_FILE_DIR + ZIP_FILE_NAME, type_of_archive, DIR_OF_UNPACKED_FILES, NAME_OF_UNZIPED_FILES
        )
        # shutil.rmtree(DIR_OF_UNPACKED_FILES+name_of_unziped_files, ignore_errors=False, onerror=None)


def unpack_files():
    print_info("Unpacking files")
    if os.path.exists(ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive):
        if os.path.exists(DIR_OF_UNPACKED_FILES + NAME_OF_UNZIPED_FILES):
            shutil.rmtree(DIR_OF_UNPACKED_FILES + NAME_OF_UNZIPED_FILES, ignore_errors=False, onerror=None)
        shutil.unpack_archive(
            ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive, DIR_OF_UNPACKED_FILES, type_of_archive
        )
        # os.remove(ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive)


def upload_to_prod_google_drive(video_path, title, main_folder_id=prod_google_grive_id):
    try:
        print_info("Uploading to prod google drive")
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_file(GOOGLE_KEY_PATH, scopes=SCOPES)
        service = build("drive", "v3", credentials=credentials)
        file_metadata = {"name": title, "parents": [main_folder_id]}
        media = MediaFileUpload(video_path, chunksize=CHUNKSIZE, resumable=True)
        r = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        return ["id"]
    except Exception as exc:
        print_error("Files was NOT uploaded to prod google drive")
        print_error(exc)
        return None


def download_from_tech_google_drive(file_id, file_path=ZIP_FILE_DIR, file_name=ZIP_FILE_NAME + "." + type_of_archive):
    try:
        print_info("Downloading from prod google drive")
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_file(GOOGLE_KEY_PATH, scopes=SCOPES)
        service = build("drive", "v3", credentials=credentials)
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_path + file_name, "wb")
        MediaIoBaseDownload()
        downloader = MediaIoBaseDownload(fh, request, chunksize=CHUNKSIZE)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        unpack_files()
        print_success("files was downloaded")
    except Exception as exc:
        print_error("Files was NOT downloaded")
        print_error(exc)
        return None


def upload_to_tech_google_drive(title, main_folder_id=tech_google_drive_id):
    try:
        print_info("Uploading to prod google drive")
        pack_files()
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_file(GOOGLE_KEY_PATH, scopes=SCOPES)
        service = build("drive", "v3", credentials=credentials)
        file_metadata = {"name": title, "parents": [main_folder_id]}
        media = MediaFileUpload(
            ZIP_FILE_DIR + ZIP_FILE_NAME + "." + type_of_archive, chunksize=CHUNKSIZE, resumable=True
        )
        r = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print_success("Files was uploaded to prod google drive")
        return r["id"]
    except Exception as exc:
        print_error("Files was NOT uploaded to prod google drive")
        print_error(exc)
        return None
