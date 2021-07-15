import os
import time
from typing import Union

import dirs
from src.db.mongo_parser.mongo_parser import MongoParser
from src.processing.core import processing_video
from src.processing.yt_download import (
    download_video_from_youtube,
    good_link,
    get_yt_object,
)
from src.processing.watermark import gen_thumbnail_with_watermark
from src.processing.yt_upload.upload import upload_video_to_youtube
from src.processing.core.time_codes import get_time_codes

parser = MongoParser()  # аргументы конструктора зависят


def prepare_for_processing(yt_object):
    dirs.create_dirs()
    downloading_res = download_video_from_youtube(
        yt_object, dirs.INPUT_VIDEO_DIR, dirs.INPUT_AUDIO_DIR, dirs.INPUT_THUMBNAIL_DIR
    )
    return downloading_res


def gen_description(yt_object, time_codes=None):
    video_credits = f"Оригинал видео: {yt_object.watch_url} с канала {yt_object.author}."
    result = f"\n{video_credits}\n"
    if time_codes:
        time_codes_fmtd = '\n'.join(f'{k}{v}' for k, v in time_codes.items())
        time_codes_str = f"Таймкоды (экспериментальная версия, возможны погрешности):\n{time_codes_fmtd}"
        result += time_codes_str

    return result


def process_link(link) -> Union[str, None]:
    yt_object = get_yt_object(link)
    if not yt_object:
        return None

    downloaded_pack = prepare_for_processing(yt_object)
    if not downloaded_pack:
        return None
    video_name, input_video_path, audio_path, input_thumbnail_path = downloaded_pack

    output_video_path = os.path.join(dirs.OUTPUT_VIDEO_DIR, video_name + ".mp4")
    output_thumbnail_path = os.path.join(dirs.OUTPUT_THUMBNAIL_DIR, "thumbnail.png")
    print('output_video_path'.upper(), output_video_path)

    description = yt_object.description

    time_codes = get_time_codes(description)
    new_time_codes_k = processing_video(input_video_path, output_video_path, audio_path, list(time_codes.keys()))
    new_time_codes = dict(zip(new_time_codes_k, time_codes.values())) if new_time_codes_k else None

    gen_thumbnail_with_watermark(input_thumbnail_path, dirs.WATERMARK_PATH, output_thumbnail_path)
    print("processing_done")
    new_video_id = upload_video_to_youtube(
        video_path=output_video_path,
        thumbnail_path=output_thumbnail_path,
        title=yt_object.title,
        description=gen_description(yt_object, new_time_codes),
        tags=yt_object.keywords,
    )
    return new_video_id


if __name__ == '__main__':
    while True:
        for video_link_object in parser.get_videos_with_status("in queue"):
            video_link = video_link_object[0]
            parser.set('video', url=video_link, status="in process")
            print(video_link + " : in process")
            try:
                if good_link(video_link):
                    result_video_id = process_link(video_link)
                    if result_video_id:
                        print('done')
                        parser.set('video', url=video_link, new_video_id=result_video_id)
                    else:
                        print('error')
                        parser.set('video', url=video_link, status="error")
                else:
                    print("error")
                    parser.set('video', url=video_link, status="error")
            except Exception as ex:
                print("error:", ex)
                parser.set('video', url=video_link, status="error")

        time.sleep(60 * 5)
