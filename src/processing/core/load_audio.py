from pydub import AudioSegment
# import librosa
from pympler import asizeof
import audio2numpy


def convert_audio_to_mp3(path, new_path):
    song = AudioSegment.from_file(path, "webm")
    song.export(new_path, format="mp3",
                bitrate="320k")


def load_audio(path):
    new_path = '.'.join(path.split('.')[::-1]) + '.mp3'
    convert_audio_to_mp3(path, new_path)
    return audio2numpy.open_audio(new_path)


# convert_audio_to_mp3(orig_path)

# y, sr = librosa.load(orig_path, sr=320)
# librosa.

load_audio(r'C:\Users\79161\PycharmProjects\PyCutBot\media\input_audio\test video.webm')
