import subprocess

from scipy.io import wavfile

from utils import change_ext
import numpy as np

def merge(silent_video: str, webm_audio: str) -> str:
    dot_idx = silent_video.rfind(".")
    sounded_video = silent_video[:dot_idx] + "_MERGED" + silent_video[dot_idx:]
    command = f'ffmpeg -i "{silent_video}" -i "{webm_audio}" -c:v copy -c:a aac "{sounded_video}"'
    subprocess.call(command, shell=True)
    # os.remove(webm_audio)
    return sounded_video


def extract_wav_from_video(sounded_video_path, wav_audio_path, sample_rate=22050):
    print(f"extracting audio from {sounded_video_path}")
    command = f'ffmpeg -i "{sounded_video_path}" -ab 160k -ac 2 -ar "{sample_rate}" -vn "{wav_audio_path}"'
    subprocess.call(command, shell=True)
    print(f"extracting done: {wav_audio_path}")


def webm2wav(silent_video_path, webm_audio_path):
    sounded_video_path = merge(silent_video_path, webm_audio_path)
    wav_audio = change_ext(webm_audio_path, ".wav")
    extract_wav_from_video(sounded_video_path, wav_audio_path=wav_audio)
    #надо это убрать, и писать в логи
    print(f"wav in {wav_audio}")
    return wav_audio

def merge_channels(audio_data):
    return np.mean(audio_data, axis = 1)

def load_audio(path):
    sample_rate, audio_data = wavfile.read(path)
    audio_data = merge_channels(audio_data)
    return audio_data, sample_rate
