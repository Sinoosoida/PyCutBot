from moviepy.editor import AudioFileClip, VideoFileClip

input_video_path = r"C:\Users\79161\PycharmProjects\PyCutBot\test_media\algo_test_media_safe\input_video\Алгоритмы и структуры данных 10 Паросочетания.mp4"
audio_path = r"C:\Users\79161\PycharmProjects\PyCutBot\test_media\algo_test_media_safe\input_audio\Алгоритмы и структуры данных 10 Паросочетания.webm"
ENDT = 13 * 60

clip = VideoFileClip(input_video_path).subclip(t_start=0, t_end=ENDT)
audioclip = AudioFileClip(audio_path).subclip(t_start=0, t_end=ENDT)
clip: VideoFileClip = clip.set_audio(audioclip)
clip.write_videofile(filename="algo_sound_13m.mp4")
