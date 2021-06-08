from pytube import YouTube
import os
import requests

image_dir = '../useful_scripts'

video_url = 'https://www.youtube.com/watch?v=AlKy1Oc0x-U&ab_channel=%D0%9F%D0%B0%D0%B2%D0%B5%D0%BB%D0%92%D0%98%D0%9A%D0%A2%D0%9E%D0%A0%D0%9F%D0%B0%D0%B2%D0%B5%D0%BB%D0%92%D0%98%D0%9A%D0%A2%D0%9E%D0%A0'
url = YouTube(video_url).thumbnail_url
full_path = os.path.join(image_dir, 'thumbnail_pav_viktor.png')
with open(full_path, 'wb') as handle:
    response = requests.get(url, stream=True)
    if not response.ok:
        print('no thumbnail')
    for block in response.iter_content(1024):
        if not block:
            break
        handle.write(block)
print('done')
