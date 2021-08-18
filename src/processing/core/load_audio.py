import librosa
import numpy as np
from pydub import AudioSegment


def convert_audio_to_mp3(path, new_path):
    song = AudioSegment.from_file(path, "webm")
    song.export(new_path, format="mp3",
                bitrate="320k")


def load_audio(path):
    new_path = '.'.join(path.split('.')[::-1]) + '.mp3'
    convert_audio_to_mp3(path, new_path)
    res = np.array([])
    stream = librosa.stream(path,
                            block_length=256,
                            frame_length=4096,
                            hop_length=1024)
    for block in stream:
        np.append(res, block)
    return res


test_path = input()
print(load_audio(test_path))
