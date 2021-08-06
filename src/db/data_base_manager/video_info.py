"https://www.googleapis.com/youtube/v3/channels"

from src.processing.yt_upload.google_api_utils import Create_Service
import os


def get_abs_path(relative_path):
    dir_name = os.path.dirname(__file__)
    return os.path.join(dir_name, relative_path)


def get_video_list(video_id, app_version=5):
    CLIENT_SECRET_FILE =get_abs_path(f'..\..\google_api\client_secrets\client_secret_{app_version}.json')
    # with open(CLIENT_SECRET_FILE, 'r+') as f:
    #     print(f.read())

    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
              'https://www.googleapis.com/auth/youtube.upload',
              'https://www.googleapis.com/auth/youtube',
              'https://www.googleapis.com/auth/youtube.readonly']

    service = Create_Service(
        CLIENT_SECRET_FILE, API_NAME, API_VERSION, app_version, SCOPES
    )

    res = service.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id,
    ).execute()

    print(res)
    print(res['items'][0].keys())

get_video_list('i_5xPDX-erE')

#
#
# # -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

# import os
#
# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import googleapiclient.errors
#
# scopes = []

# def main(app_version):
#     # Disable OAuthlib's HTTPS verification when running locally.
#     # *DO NOT* leave this option enabled in production.
#     # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
#
#     api_service_name = "youtube"
#     api_version = "v3"
#     client_secrets_file =
#
#     # Get credentials and create an API client
#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#         client_secrets_file, scopes)
#     credentials = flow.run_console()
#     youtube = googleapiclient.discovery.build(
#         api_service_name, api_version, credentials=credentials)
#
#     request = youtube.channels().list(
#         part="snippet,contentDetails,statistics",
#         id="UC_x5XG1OV2P6uZZ5FSM9Ttw"
#     )
#     response = request.execute()
#
#     print(response)
#
# if __name__ == "__main__":
#     main(5)