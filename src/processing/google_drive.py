from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def send_to_google_drive(file_path, name):
    print("send_to_google_drive".upper() + "IS DEPRECATED!!!!!!!")
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    SERVICE_ACCOUNT_FILE = "./drive-keys.json"
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=credentials)
    folder_id = "1n1Zi4KbOKQgOaoKyYuo4Vs0vARAhXsBr"
    file_metadata = {"name": name, "parents": [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields="id").execute()
