import os
import shutil
import warnings

ROOT_DIR = "./"
MEDIA_FOLDER_NAME = "media"

join = os.path.join
MEDIA_DIR = join(ROOT_DIR, MEDIA_FOLDER_NAME)
INPUT_VIDEO_DIR = join(MEDIA_DIR, "input_video")
INPUT_AUDIO_DIR = join(MEDIA_DIR, "input_audio")
INPUT_THUMBNAIL_DIR = join(MEDIA_DIR, "input_thumbnail")
OUTPUT_VIDEO_DIR = join(MEDIA_DIR, "output_video")
OUTPUT_THUMBNAIL_DIR = join(MEDIA_DIR, "output_thumbnail")
WATERMARK_PATH = "img/watermark.png"
ZIP_FILE_DIR = ROOT_DIR
ZIP_FILE_NAME = "packed_fles"
DIR_OF_UNPACKED_FILES = ROOT_DIR
NAME_OF_UNZIPED_FILES = MEDIA_FOLDER_NAME
GOOGLE_KEY_PATH = "src/processing/google_drive/google_drive_api.json"

def create_dirs():
    if os.path.exists(MEDIA_DIR):
        shutil.rmtree(MEDIA_DIR)
        warnings.warn(message="MEDIA_DIR already exists", category=UserWarning, stacklevel=1)
    os.mkdir(MEDIA_DIR)
    os.mkdir(INPUT_VIDEO_DIR)
    os.makedirs(OUTPUT_VIDEO_DIR)
    os.makedirs(INPUT_AUDIO_DIR)
    os.makedirs(INPUT_THUMBNAIL_DIR)
    os.makedirs(OUTPUT_THUMBNAIL_DIR)
