import pydub
import numpy as np


def load_audio(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_file(f, "webm")
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return np.float32(y) / 2 ** 15, a.frame_rate
    else:
        return y, a.frame_rate
