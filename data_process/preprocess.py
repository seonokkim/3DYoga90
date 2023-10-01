import cv2
import numpy as np
import mediapipe as mp
import os
import pandas as pd
import shutil
import json
from moviepy.video.io.VideoFileClip import VideoFileClip

def convert_everything_to_mp4(src_path = 'raw_videos', overwrite=False):
    # Set the destination path
    dst_path = os.path.join(os.path.dirname(src_path), 'raw_videos_mp4')

    # Create the destination folder if it doesn't exist
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    for root, _, files in os.walk(src_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_basename, extension = os.path.splitext(filename)

            if extension.lower() == '.mp4':
                # For .mp4 files, simply copy to the destination folder
                new_file_path = os.path.join(dst_path, filename)
                if overwrite or not os.path.exists(new_file_path):
                    print(f"Coping {filename} to {dst_path}")
                    shutil.copy(file_path, new_file_path)
                    print(f"Copied {filename} to {dst_path}")
                else:
                    print(f"File {filename} already exists in {dst_path}. Skipping.")
            else:
                try:
                    # For non-.mp4 files, rename the extension to .mp4
                    new_filename = file_basename + ".mp4"
                    new_file_path = os.path.join(dst_path, new_filename)
                    if overwrite or not os.path.exists(new_file_path):
                        print(f"Converting {filename} to {new_filename}")
                        shutil.copy(file_path, new_file_path)
                        print(f"Converted {filename} to {new_filename}")
                    else:
                        print(f"File {new_filename} already exists in {dst_path}. Skipping.")
                except Exception as e:
                    print(f"Failed to convert {filename}: {str(e)}")


def cut_videos_from_json(json_file = '3DYoga90.json', videos_folder='trimmed_mp4', src_video_path ='raw_videos_mp4'):
    content = json.load(open(json_file))

    
    if not os.path.exists(videos_folder):
        os.mkdir(videos_folder)

    for entry in content:
        instances = entry['instances']

        for inst in instances:
            url = inst['url']
            start_frame = inst['start_frame'] - 1
            end_frame = inst['end_frame'] - 1

            yt_identifier = url[-11:]
            src_videos = os.path.join(src_video_path, yt_identifier + '.mp4')
            video_id = str(inst['sequence_id'])  # Convert video_id to string
            dst_videos = os.path.join(videos_folder, video_id + '.mp4')

            # Skip if the video file already exists
            if os.path.exists(dst_videos):
                print(f'Skipping video {video_id} - already exists.')
                continue

            # Check if the source video file exists
            if not os.path.exists(src_videos):
                print(f'Skipping video {video_id} - source video file not found.')
                continue

            try:
                # Use moviepy to cut the video
                clip = VideoFileClip(src_videos).subclip(start_frame, end_frame)
                clip.write_videofile(dst_videos)

                print(f'Video {video_id} cut and saved to {dst_videos}')

            except Exception as e:
                print(f'Failed to cut video {video_id}: {str(e)}')


def main():
    # 1. Convert .swf, .mkv file to mp4.
    convert_everything_to_mp4()

    # 2. Cut the videos and create sequences.
    cut_videos_from_json()


if __name__ == "__main__":
    main()