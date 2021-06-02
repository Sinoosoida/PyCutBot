from moviepy.editor import *
from moviepy.editor import VideoFileClip, concatenate_videoclips
import librosa
import numpy as np


def decouple_audio(video_name, audio_name):
    clip = VideoFileClip(video_name)
    original_audio = clip.audio
    original_audio.write_audiofile(audio_name)
    clip.reader.__del__()
    clip.audio.reader.__del__()


def detect_loud_frames(audio_array, number_of_frames, limit):
    frames = []
    for i in range(0, number_of_frames):
        a = (audio_array[int(len(audio_array) * i / number_of_frames):int(
            len(audio_array) * (i + 1) / number_of_frames)] ** 2).mean()
        if a > limit:
            frames.append(True)
        else:
            frames.append(False)
    return frames


def add_frames(frames, prev_frames=0, post_frames=0):
    for i in range(0, len(frames)):
        if frames[i] and (i - prev_frames >= 0):
            frames[i - prev_frames] = True
    frames = frames[::-1]
    for i in range(0, len(frames)):
        if frames[i] and (i - post_frames >= 0):
            frames[i - post_frames] = True
    frames = frames[::-1]
    return frames


def delete_short_cuts(cuts, number_of_frames_limit=0):  # готово
    tmp_cuts = []
    for i in range(len(cuts)):
        if (cuts[i][1] - cuts[i][0]) >= number_of_frames_limit:
            tmp_cuts.append(cuts[i])
    return tmp_cuts


def make_cuts(frames):
    cuts = []
    place = 0
    expect = None
    for i in range(0, len(frames)):
        if expect is None:
            expect = frames[i]
            place = i
        else:
            if (not expect) and frames[i]:
                expect = frames[i]
                place = i
            if expect and (not frames[i]):
                cuts.append([place, i - 1])
                expect = frames[i]
    if expect:
        cuts.append([place, len(frames) - 1])
    return cuts


def processing_audio(number_of_frames, name="audio.wav", limit_coefficient=1, prev_frames=0, post_frames=0,
                     number_of_frames_limit=0):
    audio_array, sample_rate = librosa.load(name)
    time_of_audio = len(audio_array) / sample_rate
    volume_limit = np.median(audio_array ** 2) * limit_coefficient
    frames = detect_loud_frames(audio_array, number_of_frames, volume_limit)
    frames = add_frames(frames, prev_frames, post_frames)
    cuts = make_cuts(frames)
    cuts = delete_short_cuts(cuts, number_of_frames_limit)
    return cuts


def processing_video(video_path, new_path, audio_path):
    print(video_path)
    print(new_path)
    print(audio_path)
    clip = VideoFileClip(video_path)
    print("video_d_done")
    audioclip = AudioFileClip(audio_path)
    print("audio_d_done")
    clip = clip.set_audio(audioclip)
    print("merging_done")
    duration = clip.duration
    number_of_frames = clip.reader.nframes
    cuts = processing_audio(number_of_frames, audio_path, 1.25, 1, 1, 5)
    print("audio_processing_done")
    clips = []
    for i in cuts:
        clips.append(clip.subclip(i[0] * duration / number_of_frames, i[1] * duration / number_of_frames))
    final = concatenate_videoclips(clips).write_videofile(new_path)
    clip.reader.__del__()
    clip.audio.reader.__del__()
    print("done")
    # audioclip.reader.__del__()
    # audioclip.audio.reader.__del__
