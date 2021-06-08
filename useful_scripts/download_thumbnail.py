from pytube import YouTube
import os
import requests

image_dir = '../useful_scripts'

video_url = 'https://youtu.be/wLWgQnmqTvY'
url = YouTube(video_url).thumbnail_url
full_path = os.path.join(image_dir, 'thumbnail_prik.png')
with open(full_path, 'wb') as handle:
    response = requests.get(url, stream=True)
    if not response.ok:
        print('no thumbnail')
    for block in response.iter_content(1024):
        if not block:
            break
        handle.write(block)
print('done')
