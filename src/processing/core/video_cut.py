import librosa
import numpy as np
from moviepy.editor import *
from moviepy.editor import VideoFileClip, concatenate_videoclips
from src.processing.core.time_codes import get_new_time_codes


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
    return np.array(tmp_cuts)


def make_cuts(frames):
    cuts = []
    place = 0
    expect = None

    for frame_idx in range(0, len(frames)):
        if expect is None:
            expect = frames[frame_idx]
            place = frame_idx
        else:
            if (not expect) and frames[frame_idx]:
                expect = frames[frame_idx]
                place = frame_idx
            if expect and (not frames[frame_idx]):
                cuts.append([place, frame_idx - 1])
                expect = frames[frame_idx]
    if expect:
        cuts.append([place, len(frames) - 1])
    print('CUTS:', cuts)
    return cuts


def processing_audio(number_of_frames, name="audio.wav", limit_coefficient=1, prev_frames=0, post_frames=0,
                     number_of_frames_limit=0):
    audio_array, sample_rate = librosa.load(name)
    volume_limit = np.median(audio_array ** 2) * limit_coefficient
    frames = detect_loud_frames(audio_array, number_of_frames, volume_limit)
    frames = add_frames(frames, prev_frames, post_frames)
    cuts = make_cuts(frames)
    cuts = delete_short_cuts(cuts, number_of_frames_limit)
    return cuts


def processing_video(input_video_path, output_video_path, audio_path, time_codes=None) -> list:
    print(input_video_path)
    print(output_video_path)
    print(audio_path)
    clip = VideoFileClip(input_video_path)
    fps = clip.fps
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
    concatenate_videoclips(clips).write_videofile(output_video_path)
    clip.reader.__del__()
    clip.audio.reader.__del__()
    print("done")

    if time_codes:
        new_time_codes = get_new_time_codes(cuts, time_codes, fps)
        return new_time_codes
