from networking import *
from db import SQLParser


def links_from_lists(data_base):
    for i in data_base.get_with_status(2, 'in queue'):
        try:
            playlist = Playlist(i[0])
            for video_url in playlist.video_urls:
                data_base.save(1, str(video_url), 'in queue')
            done = True
            fail = False
            for video_url in playlist.video_urls:
                ptr_status = data_base.get_status(1, str(video_url))
                if ('fail' in ptr_status) or ('error' in ptr_status):
                    fail = True
                if ptr_status != 'done':
                    done = False
                if fail:
                    data_base.set_status(2, i[0], 'fail')
                else:
                    if done:
                        data_base.set_status(2, i[0], 'done')
                    else:
                        data_base.set_status(2, i[0], 'in process')
        except Exception as e:
            data_base.set_status(2, i[1], 'error:' + str(e))