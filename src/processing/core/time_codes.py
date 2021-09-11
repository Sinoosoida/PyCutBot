import time
import re
from log import *
from src.processing.core.frame_codes import get_new_frame_codes


def time2frame(time_code: int, fps: int):
    return time_code * fps


def frame2time(frame_code: int, fps: int):
    return time.strftime("%H:%M:%S", time.gmtime(frame_code / fps))


def get_time_codes(text: str):
    try:
        parsed_list = re.findall(r'(\d{1,2})(?::(\d{1,2}))?(?::(\d{1,2}))?[ -]*(.+)', text)
        time_codes = {}
        for a, b, c, text in parsed_list:
            a, b = int(a), int(b)
            h, m, s = (a, b, int(c)) if c and c.isdigit() else (0, a, b)
            time_codes[h * 3600 + m * 60 + s] = text
        return time_codes
    except Exception as ex:
        print_error("find_timecodes exception", ex)


def get_new_time_codes(cuts, time_codes, fps):
    frame_codes = [time2frame(tc, fps) for tc in time_codes]
    new_frame_codes = get_new_frame_codes(cuts, frame_codes)
    new_time_codes = [frame2time(fc, fps) for fc in new_frame_codes]
    return new_time_codes
