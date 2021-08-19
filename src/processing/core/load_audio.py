from scipy.io import wavfile
import subprocess
from utils import change_ext


def merge(silent_video: str, webm_audio: str) -> str:
    dot_idx = silent_video.rfind('.')
    sounded_video = silent_video[:dot_idx] + '_MERGED' + silent_video[dot_idx:]
    command = f"ffmpeg -i {silent_video} -i {webm_audio} -c:v copy -c:a aac {sounded_video}"
    subprocess.call(command, shell=True)
    # os.remove(webm_audio)
    return sounded_video


def extract_wav_from_video(sounded_video_path, wav_audio_path, sample_rate=22050):
    command = f"ffmpeg -i {sounded_video_path} -ab 160k -ac 2 -ar {sample_rate} -vn {wav_audio_path}"
    subprocess.call(command, shell=True)


def webm2wav(silent_video_path, webm_audio_path):
    sounded_video_path = merge(silent_video_path, webm_audio_path)
    wav_audio = change_ext(webm_audio_path, '.wav')
    extract_wav_from_video(sounded_video_path, wav_audio_path=wav_audio)
    return wav_audio


def load_audio(path):
    sample_rate, audio_data = wavfile.read(path)
    return audio_data, sample_rate
