from db import *
from core import *
from networking import download, send_to_google_drive, good_link, get_yt_object
from uploading import upload_video_to_youtube
from data_base_manager import *
import warnings
import os
import shutil

data_base = SQLParser()
data_base.create_db()


def prepare_for_processing(yt_object):
    if os.path.exists('./media'):
        shutil.rmtree("./media")
        warnings.warn(message="media already exists", category=UserWarning, stacklevel=1)
        os.mkdir('media')
        os.mkdir("./media/core")
        os.makedirs("./media/new_video")
        os.makedirs("./media/audio")
        os.makedirs("./media/thumbnail")
        return download(yt_object, "./media/core", "./media/audio", "./media/thumbnail")


def add_credits_to_description(text, link, author):
    video_credits = f"Оригинал видео: {link} с канала {author}"
    return text + f"\n{video_credits}"


def process_link(link):
    yt_object = get_yt_object(link)
    video_name, video_path, audio_path, thumbnail_path = prepare_for_processing(yt_object)
    new_video_path = "./media/new_video/core.mp4"
    processing_video(video_path, new_video_path, audio_path)
    print("processing_done")
    send_to_google_drive(new_video_path, video_name + ".mp4")
    print("saving to google drive done")
    upload_video_to_youtube(video_path=new_video_path,
                            thumbnail_path=thumbnail_path,
                            title=yt_object.title,
                            description=add_credits_to_description(yt_object.description,
                                                                   link,
                                                                   yt_object.author),
                            tags=yt_object.keywords)


while True:
    for video_link_object in data_base.get_video_with_status('in queue'):
        if not video_link_object:
            continue
        video_link = video_link_object[0]
        data_base.set_status(video_link, 'in process')
        print(video_link + ' : in process')
        try:
            if good_link(video_link):
                process_link(video_link)
                print('done')
                data_base.set_status(video_link, "done")
            else:
                print('error')
                data_base.set_status(video_link, "error")
        except Exception as ex:
            print('error:', ex)
            data_base.set_status(video_link, "error")
