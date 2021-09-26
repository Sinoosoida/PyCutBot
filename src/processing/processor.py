import json
import os
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

import dirs
import requests as req

from log import *
from src.config import mongo_password, mongo_username
from src.db.mongo_parser.mongo_parser import MongoParser
from src.processing.core import processing_video
from src.processing.core.time_codes import get_time_codes
from src.processing.google_drive.google_drive import upload_to_prod_google_drive, upload_to_tech_google_drive
from src.processing.watermark import gen_thumbnail_with_watermark
from src.processing.yt_download import download_video_from_youtube, get_yt_object, good_link, get_clear_name
from src.processing.yt_upload.upload import upload_video_to_youtube

parser = MongoParser(atlas=True, username=mongo_username, password=mongo_password)


def get_abs_path(relative_path):
    dir_name = os.path.dirname(__file__)
    return os.path.join(dir_name, relative_path)


def prepare_for_processing(yt_object):
    try:
        dirs.create_dirs()
    except Exception as exc:
        print("creating dirs ex: ", exc)
    downloading_res = download_video_from_youtube(
        yt_object, dirs.INPUT_VIDEO_DIR, dirs.INPUT_AUDIO_DIR, dirs.INPUT_THUMBNAIL_DIR
    )
    return downloading_res


def gen_description(yt_object, time_codes=None):
    video_credits = f"Оригинал видео: {yt_object.watch_url} с канала {yt_object.author}."
    result = f"\n{video_credits}\n"
    if time_codes:
        time_codes_fmtd = "\n".join(f"{k}{v}" for k, v in time_codes.items())
        time_codes_str = f"Таймкоды (экспериментальная версия, возможны погрешности):\n{time_codes_fmtd}"
        result += time_codes_str

    return result


def process_link(link):
    start_time = time.time()
    yt_object = get_yt_object(link)
    if not yt_object:
        print_error("Cannot create YouTube object")
        return None, "pytube error"

    print_info("Downloading...")
    downloaded_pack = prepare_for_processing(yt_object)
    if not downloaded_pack:
        print_error("Cannot download")
        return None, "download error"
    video_name, input_video_path, audio_path, input_thumbnail_path = downloaded_pack
    print_success("Downloading done")

    output_video_path = os.path.join(dirs.OUTPUT_VIDEO_DIR, video_name + ".mp4")
    output_thumbnail_path = os.path.join(dirs.OUTPUT_THUMBNAIL_DIR, "thumbnail.png")

    description = yt_object.description

    time_codes = get_time_codes(description)
    print_info(f"Time codes: {time_codes}")

    #This is where video processing takes place
    new_time_codes_k = processing_video(
        input_video_path,
        output_video_path,
        audio_path,
        time_codes.keys() if time_codes else None,
    )
    new_time_codes = dict(zip(new_time_codes_k, time_codes.values())) if new_time_codes_k else None
    print_info(f"New time codes: {new_time_codes}")

    print_info("Generating watermark...")
    gen_thumbnail_with_watermark(input_thumbnail_path, dirs.WATERMARK_PATH, output_thumbnail_path)
    print_success("Generating watermark done")

    tech_gd_id, yt_id, prod_gd_id = None, None, None

    with open(get_abs_path("../upload_config.json")) as c:
        config = json.load(c)
        yt_load = config.get("youtube")
        gdrive_load = config.get("gdrive")

    try:
        tech_gd_id = upload_to_tech_google_drive(title=get_clear_name(yt_object))
    except Exception as exc:
        print_error(exc)
        return None, "tech gdrive upload error"

    if gdrive_load:
        try:
            prod_gd_id = upload_to_prod_google_drive(video_path=output_video_path, title=get_clear_name(yt_object))
        except Exception as exc:
            print_error(exc)
            return None, "prod gdrive upload error"

    if yt_load:
        try:
            yt_id = upload_video_to_youtube(
                video_path=output_video_path,
                thumbnail_path=output_thumbnail_path,
                title=yt_object.title,
                description=gen_description(yt_object, new_time_codes),
                tags=yt_object.keywords,
            )
        except Exception as exc:
            print_error(exc)
            return None, "youtube upload error"

    print_info(f"Full processing done in {round(time.time() - start_time, 2)}s (video len={yt_object.length}s)")
    return tech_gd_id, yt_id, prod_gd_id, None


sleep_time = 5

from telegram import Bot

# костыль, да

bot = Bot(token='739844988:AAHEHt8KiT9czNUFJuvqXUgfJOOzDVGnJ70')  # @Geneticist_bot


def send_error(text):
    for chat_id in [496233529, 423216896]:
        try:
            bot.send_message(chat_id=chat_id, text=text)
        except Exception as ex:
            print(ex)


def main():
    while True:
        for video_obj in parser.get_videos_with_status("in queue"):
            video_link = video_obj.url
            parser.set("video", url=video_link, status="processing")
            print_header1_info(f"Processing {video_link}")
            try:
                if good_link(video_link):
                    res_tech_gd_id, res_yt_id, res_prod_gd_id, error_str = process_link(video_link)
                    if not error_str:
                        print_success("Uploading done")
                        print_success(f"Processing {video_link} done")
                        parser.set(
                            "video",
                            url=video_link,
                            new_video_id=res_yt_id,
                            tech_gd_folder_id=res_tech_gd_id,
                            prod_gd_file_id=res_prod_gd_id,
                            status="done",
                            status_info="success",
                        )
                    else:
                        print_error(f"Uploading {video_link} error: {error_str}")
                        parser.set(
                            "video",
                            url=video_link,
                            status="error",
                            status_info=error_str,
                        )
                        send_error(error_str)
                else:
                    print_error(f"Bad link: {video_link}")
                    parser.set("video", url=video_link, status="error", status_info="bad link")
                    send_error("bad link")
            except Exception as ex:
                print_error(f"Supreme error on {video_link}: {ex}")
                parser.set("video", url=video_link, status="error", status_info="unknown")
                send_error(str(ex))
                send_error(str(traceback.format_exc()))
                traceback.print_exc()
            print_sep()
        time.sleep(sleep_time)


def down_detector():
    while True:
        try:
            req.get(f"http://51.15.75.62:5000/upd?service=pycutbot_processor&time_delta={sleep_time}")
        except Exception as ex:
            print_error("DOWNDETECTOR EX", ex)
        time.sleep(sleep_time)


if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        main_future = executor.submit(main)
        down_detector_future = executor.submit(down_detector)
