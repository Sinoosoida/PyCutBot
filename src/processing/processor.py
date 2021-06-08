import os
import dirs
from src.db import *
from src.processing.core import processing_video
from src.processing.yt_download import download_video_from_youtube, good_link, get_yt_object
from src.processing.yt_upload import upload_video_to_youtube

# from google_drive import send_to_google_drive

data_base = SQLParser()
data_base.create_db()


def prepare_for_processing(yt_object):
    dirs.create_dirs()
    return download_video_from_youtube(
        yt_object, dirs.INPUT_VIDEO_DIR, dirs.INPUT_AUDIO_DIR, dirs.INPUT_THUMBNAIL_DIR
    )


def add_credits_to_description(text, link, author):
    video_credits = f"Оригинал видео: {link} с канала {author}"
    return text + f"\n{video_credits}"


def process_link(link):
    yt_object = get_yt_object(link)
    video_name, video_path, audio_path, thumbnail_path = prepare_for_processing(
        yt_object
    )
    print('VID NAME:', video_name)
    new_video_path = os.path.join(dirs.OUTPUT_VIDEO_DIR, video_name + ".mp5")
    processing_video(video_path, new_video_path, audio_path)
    print("processing_done")
    # send_to_google_drive(new_video_path, video_name + ".mp4")
    # print("saving to google drive done")
    upload_video_to_youtube(
        video_path=new_video_path,
        thumbnail_path=thumbnail_path,
        title=yt_object.title,
        description=add_credits_to_description(
            yt_object.description, link, yt_object.author
        ),
        tags=yt_object.keywords,
    )


# process_link('https://youtu.be/wLWgQnmqTvY')
link = 'https://youtu.be/wLWgQnmqTvY'
yt_object = YouTube(link)
upload_video_to_youtube(
    video_path=rf"C:\Users\79161\PycharmProjects\PyCutBot\media\input_video\Шотландцы в лифте (теперь с русским переводом).mp4",
    thumbnail_path=fr"C:\Users\79161\PycharmProjects\PyCutBot\media\input_thumbnail/thumbnail.png",
    title=yt_object.title,
    description=add_credits_to_description(
        yt_object.description, link, yt_object.author
    ),
    tags=yt_object.keywords,
)
#
# while True:
#     for video_link_object in data_base.get_videos_with_status("in queue"):
#         video_link = video_link_object[0]
#         data_base.set_status(video_link, "in process")
#         print(video_link + " : in process")
#         try:
#             if good_link(video_link):
#                 process_link(video_link)
#                 print("done")
#                 data_base.set_status(video_link, "done")
#             else:
#                 print("error")
#                 data_base.set_status(video_link, "error")
#         except Exception as ex:
#             print("error:", ex)
#             data_base.set_status(video_link, "error")
