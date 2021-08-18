from pydub import AudioSegment
# import librosa
from pympler import asizeof
import audio2numpy


def convert_audio_to_mp3(path):
    song = AudioSegment.from_file(path, "mp3")
    song.export(path, format="mp3",
                bitrate="320k")


def load_audio(path):
    convert_audio_to_mp3(path)
    return audio2numpy.open_audio(path)

# convert_audio_to_mp3(orig_path)

# y, sr = librosa.load(orig_path, sr=320)
# librosa.
