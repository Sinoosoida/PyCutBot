from db import *
from video import *
from networking import *
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
    os.mkdir("./media/video")
    os.makedirs("./media/new_video")
    os.makedirs("./media/audio")
    video_name = get_name(link)
    print(video_name)
    video_path = download_video(link, "./media/video")
    print(video_path)
    audio_path = download_audio(link, "./media/audio")
    print(video_path)
    if audio_path is None:
        warnings.warn(message="have not audio", category=UserWarning, stacklevel=1)
    if video_path is None:
        warnings.warn(message="have not audio", category=UserWarning, stacklevel=1)
    print(str(video_path) + " " + str(audio_path))
    print("downloading done")
    return video_name, video_path, audio_path


def process_link(link):
    video_name, video_path, audio_path = prepare_for_processing(link)
    new_path = "./media/new_video/video.mp4"
    processing_video(video_path, new_path, audio_path)
    print("processing_done")
    send_to_google_drive(new_path, video_name + ".mp4")
    print("saving done")


while True:
    links_from_lists(data_base)
    for i in data_base.get_with_status(1, 'in queue'):
        data_base.set_status(1, i[0], 'in process')
        print(i[0] + ' : in process')
        try:
            if good_link(i[0]):
                process_link(i[0])
                print('done')
                data_base.set_status(1, i[0], "done")
            else:
                print('error')
                data_base.set_status(1, i[0], "error")
        except:
            print('error')
            data_base.set_status(1, i[0], "error")
