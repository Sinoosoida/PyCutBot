from db import *
from core import *
from networking import download, send_to_google_drive, good_link
from data_base_handler import *
import warnings
import os
import shutil

data_base = SQLParser()
data_base.create_db()


def prepare_for_processing(link):
    if os.path.exists('./media'):
        shutil.rmtree("./media")
        warnings.warn(message="media already exists", category=UserWarning, stacklevel=1)
    os.mkdir('media')
    os.mkdir("./media/core")
    os.makedirs("./media/new_video")
    os.makedirs("./media/audio")
    return download(link, "./media/core", "./media/audio")


def process_link(link):
    video_name, video_path, audio_path, yt_object = prepare_for_processing(link)
    new_path = "./media/new_video/core.mp4"
    processing_video(video_path, new_path, audio_path)
    print("processing_done")
    send_to_google_drive(new_path, video_name + ".mp4")
    print("saving to google drive done")


while True:
    links_from_lists(data_base)
    for video_link_object in data_base.get_with_status(1, 'in queue'):
        video_link = video_link_object[0]
        data_base.set_status(1, video_link, 'in process')
        print(video_link + ' : in process')
        try:
            if good_link(video_link):
                process_link(video_link)
                print('done')
                data_base.set_status(1, video_link, "done")
            else:
                print('error')
                data_base.set_status(1, video_link, "error")
        except Exception as ex:
            print('error:', ex)
            data_base.set_status(1, video_link, "error")
