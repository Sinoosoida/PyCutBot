import os
import shutil
import warnings

MEDIA_DIR = '../../media'

join = os.path.join
INPUT_VIDEO_DIR = join(MEDIA_DIR, "input_video")
INPUT_AUDIO_DIR = join(MEDIA_DIR, "input_audio")
INPUT_THUMBNAIL_DIR = join(MEDIA_DIR, "input_thumbnail")
OUTPUT_VIDEO_DIR = join(MEDIA_DIR, "output_video")
OUTPUT_THUMBNAIL_DIR = join(MEDIA_DIR, "output_thumbnail")
WATERMARK_PATH = "../img/watermark.png"


def create_dirs():
    if os.path.exists(MEDIA_DIR):
        shutil.rmtree(MEDIA_DIR)
        warnings.warn(
            message="MEDIA_DIR already exists", category=UserWarning, stacklevel=1
        )
    os.mkdir(MEDIA_DIR)
    os.mkdir(INPUT_VIDEO_DIR)
    os.makedirs(OUTPUT_VIDEO_DIR)
    os.makedirs(INPUT_AUDIO_DIR)
    os.makedirs(INPUT_THUMBNAIL_DIR)
    os.makedirs(OUTPUT_THUMBNAIL_DIR)
