from google.oauth2 import service_account
from google.protobuf import service
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
import pprint
import os

import google.oauth2
# import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io
import shutil

zip_file_dir = "../"
zip_file_name = "packed_fles"
dir_of_unpacked_files = "../"
name_of_unziped_files = "media"
type_of_archive = "zip"
keys_path = "google_drive_api.json"


def pack_files():
    if os.path.exists(dir_of_unpacked_files + name_of_unziped_files):
        if os.path.exists(zip_file_dir + zip_file_name + "." + type_of_archive):
            os.remove(zip_file_dir + zip_file_name + "." + type_of_archive)
        shutil.make_archive(zip_file_dir + zip_file_name,
                            type_of_archive,
                            dir_of_unpacked_files,
                            name_of_unziped_files)
        # shutil.rmtree(dir_of_unpacked_files+name_of_unziped_files, ignore_errors=False, onerror=None)


def unpack_files():
    if os.path.exists(zip_file_dir + zip_file_name + "." + type_of_archive):
        if os.path.exists(dir_of_unpacked_files + name_of_unziped_files):
            shutil.rmtree(dir_of_unpacked_files + name_of_unziped_files, ignore_errors=False, onerror=None)
        shutil.unpack_archive(zip_file_dir + zip_file_name + "." + type_of_archive, dir_of_unpacked_files,
                              type_of_archive)
        # os.remove(zip_file_dir + zip_file_name + "." + type_of_archive)


def upload_to_pub_google_drive(video_path, title, main_folder_id="1PGHW4Crd2PYZdhIZT8a69pG4Di7Q6gn7"):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        keys_path, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    file_metadata = {
        'name': title,
        'parents': [main_folder_id]
    }
    media = MediaFileUpload(video_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(r)
    return (r)


def download_from_prod_google_drive(file_id, file_path=zip_file_dir, file_name=zip_file_name+"."+type_of_archive):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_path+file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


def upload_to_prod_google_drive(title, main_folder_id="1PGHW4Crd2PYZdhIZT8a69pG4Di7Q6gn7"):
    pack_files()
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        keys_path, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    file_metadata = {
        'name': title,
        'parents': [main_folder_id]
    }
    media = MediaFileUpload(zip_file_dir + zip_file_name + "." + type_of_archive, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(r)
    return (r)


# pack_files()
upload_to_prod_google_drive("tets")
