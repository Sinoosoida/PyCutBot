import librosa
import numpy as np

import subprocess
import os
from utils import change_ext


def merge(silent_video: str, webm_audio: str) -> str:
    dot_idx = silent_video.rfind('.')
    sounded_video = silent_video[:dot_idx] + '_MERGED' + silent_video[dot_idx:]
    command = f"ffmpeg -i {silent_video} -i {webm_audio} -c:v copy -c:a aac {sounded_video}"
    subprocess.call(command, shell=True)
    os.remove(silent_video)
    os.remove(webm_audio)
    return sounded_video


def extract_wav_from_video(sounded_video_path, wav_audio_path, sample_rate=22050):
    command = f"ffmpeg -i {sounded_video_path} -ab 160k -ac 2 -ar {sample_rate} -vn {wav_audio_path}"
    subprocess.call(command, shell=True)


def webm2wav(silent_video_path, webm_audio_path):
    sounded_video_path = merge(silent_video_path, webm_audio_path)
    wav_audio = change_ext(webm_audio_path, '.wav')
    extract_wav_from_video(sounded_video_path, wav_audio_path=wav_audio)
    return wav_audio


from scipy.io import wavfile


def load_audio(path):
    sample_rate, audio_data = wavfile.read(path)
    return audio_data, sample_rate

# test_path = r'C:\Users\79161\PycharmProjects\PyCutBot\media\input_audio\test video.webm'
# new_path = r'C:\Users\79161\PycharmProjects\PyCutBot\media\input_audio\test video.mp3'

# convert_audio_to_mp3(test_path, new_path)
# # print(load_audio(test_path))
#
# import soundfile as sf
#
# def read_audio_section(filename, start_time, stop_time):
#     track = sf.SoundFile(filename)
#
#     can_seek = track.seekable() # True
#     if not can_seek:
#         raise ValueError("Not compatible with seeking")
#
#     sr = track.samplerate
#     start_frame = sr * start_time
#     frames_to_read = sr * (stop_time - start_time)
#     track.seek(start_frame)
#     audio_section = track.read(frames_to_read)
#     return audio_section, sr
#
# read_audio_section(test_path, 0, 1)
