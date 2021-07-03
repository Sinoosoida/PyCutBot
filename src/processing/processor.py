import os
import time
import dirs
from src.db import *
from src.processing.core import processing_video
from src.processing.yt_download import (
    download_video_from_youtube,
    good_link,
    get_yt_object,
)
from src.processing.watermark import gen_thumbnail_with_watermark
from src.processing.yt_upload import upload_video_to_youtube
from src.processing.core.time_codes import get_time_codes

data_base = SQLParser()
data_base.create_db()


def prepare_for_processing(yt_object):
    dirs.create_dirs()
    downloading_res = download_video_from_youtube(
        yt_object, dirs.INPUT_VIDEO_DIR, dirs.INPUT_AUDIO_DIR, dirs.INPUT_THUMBNAIL_DIR
    )
    return downloading_res


def gen_description(yt_object, time_codes=None):
    video_credits = f"Оригинал видео: {yt_object.watch_url} с канала {yt_object.author}."
    time_codes_fmtd = '\n'.join(f'{k}{v}' for k, v in time_codes.items())
    time_codes_str = f"Таймкоды (экспериментальная версия, возможны погрешности):\n{time_codes_fmtd}"

    return f"\n{video_credits}\n{time_codes_str}"


def process_link(link):
    yt_object = get_yt_object(link)
    if not yt_object:
        return False

    downloaded_pack = prepare_for_processing(yt_object)
    if not downloaded_pack:
        return False
    video_name, input_video_path, audio_path, input_thumbnail_path = downloaded_pack

    output_video_path = os.path.join(dirs.OUTPUT_VIDEO_DIR, video_name + ".mp4")
    output_thumbnail_path = os.path.join(dirs.OUTPUT_THUMBNAIL_DIR, "thumbnail.png")
    print('output_video_path'.upper(), output_video_path)

    description = yt_object.description

    time_codes = get_time_codes(description)
    new_time_codes_v = processing_video(input_video_path, output_video_path, audio_path, list(time_codes.keys()))

    gen_thumbnail_with_watermark(input_thumbnail_path, dirs.WATERMARK_PATH, output_thumbnail_path)
    print("processing_done")
    upload_video_to_youtube(
        video_path=output_video_path,
        thumbnail_path=output_thumbnail_path,
        title=yt_object.title,
        description=gen_description(yt_object, dict(zip(new_time_codes_v, time_codes.values()))),
        tags=yt_object.keywords,
    )
    return True


if __name__ == '__main__':
    while True:
        for video_link_object in data_base.get_videos_with_status("in queue"):
            video_link = video_link_object[0]
            data_base.set_status(video_link, "in process")
            print(video_link + " : in process")
            try:
                if good_link(video_link):
                    res = process_link(video_link)
                    if res:
                        print('done')
                    else:
                        print('error')
                        data_base.set_status(video_link, "error")
                else:
                    print("error")
                    data_base.set_status(video_link, "error")
            except Exception as ex:
                print("error:", ex)
                data_base.set_status(video_link, "error")

        time.sleep(60 * 5)
