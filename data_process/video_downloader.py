import json
import os
import time
import random


# Set this to youtube-dl if you want to use youtube-dl.

youtube_downloader = "yt-dlp"

def download_yt_videos(indexfile, saveto='raw_videos', n_videos = 5526):
    content = json.load(open(indexfile))

    if not os.path.exists(saveto):
        os.mkdir(saveto)

    #total_videos = n_videos
    downloaded_videos = 0

    for entry in content:
        pose = entry['pose']
        instances = entry['instances']

        for inst in instances:
            video_url = inst['url']
            video_id = inst['sequence_id']

            if 'youtube' not in video_url and 'youtu.be' not in video_url:
                continue

            if os.path.exists(os.path.join(saveto, video_url[-11:] + '.mp4')) or os.path.exists(os.path.join(saveto, video_url[-11:] + '.mkv')):
                print('YouTube videos {} already exists.'.format(video_url))
                continue
            else:
                cmd = f"{youtube_downloader} \"{{}}\" -o \"{{}}%(id)s.%(ext)s\""
                cmd = cmd.format(video_url, saveto + os.path.sep)

                rv = os.system(cmd)

                if not rv:
                    print(f'Finish downloading youtube video url {video_url}')
                else:
                    print(f'Unsuccessful downloading - youtube video url {video_url}')

                downloaded_videos += 1
                progress = (downloaded_videos / n_videos) * 100
                print(f'Video {video_id} downloaded successfully! Progress: {progress:.2f}%')
                # please be nice to the host - take pauses and avoid spamming
                time.sleep(random.uniform(1.0, 1.5))


if __name__ == '__main__':
  download_yt_videos('3DYoga90.json')
