import time

from log import *
from src.processing.core.frame_codes import get_new_frame_codes


def time2frame(time_code: str, fps: int):
    h, m, s = time_code.split(":")
    total_seconds = int(h) * 3600 + int(m) * 60 + int(s)
    return total_seconds * fps


def frame2time(frame_code: int, fps: int):
    return time.strftime("%H:%M:%S", time.gmtime(frame_code / fps))


def _check_buff_8(b):
    return (
        b[2] == ":"
        and b[5] == ":"
        and b[0:2].isdigit()
        and b[3:5].isdigit()
        and b[6:].isdigit()
        and int(b[3:5]) <= 60
        and int(b[6:]) <= 60
    )


def _check_buff_7(b):
    return (
        b[1] == ":"
        and b[4] == ":"
        and b[0].isdigit()
        and b[2:4].isdigit()
        and b[5:].isdigit()
        and int(b[2:4]) <= 60
        and int(b[5:]) <= 60
    )


def _find_time_codes(text: str, buff_len: int, buff_check):
    time_codes = {}
    for line in text.split("\n"):
        buffer = line[:buff_len]
        for idx, letter in enumerate(line[buff_len:]):
            if buff_check(buffer):
                time_codes[buffer] = line[buff_len + idx :]
            buffer = buffer[1:]
            buffer += letter
    return time_codes


def get_time_codes(text: str):
    try:
        tc1 = _find_time_codes(text, 8, _check_buff_8)
        if tc1:
            return tc1
        tc2 = _find_time_codes(text, 7, _check_buff_7)
        if tc2:
            return tc2
    except Exception as ex:
        print_error("find_timecodes exception", ex)


def get_new_time_codes(cuts, time_codes, fps):
    frame_codes = [time2frame(tc, fps) for tc in time_codes]
    new_frame_codes = get_new_frame_codes(cuts, frame_codes)
    if not new_frame_codes:
        return None
    new_time_codes = [frame2time(fc, fps) for fc in new_frame_codes]
    return new_time_codes
