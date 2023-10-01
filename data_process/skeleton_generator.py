import cv2
import numpy as np
import mediapipe as mp
import os
import pandas as pd
import importlib



mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose

nb_helpers = importlib.import_module("mediapipe-python.nb_helpers")
poselandmarks_list = nb_helpers.poselandmarks_list

num = 0
for i in mp_holistic.POSE_CONNECTIONS:
    if num < 5:
        print(poselandmarks_list[i[0]], '-->', poselandmarks_list[i[1]])
    else:
        break
    num += 1



def create_data_from_video(video_file):
    cap = cv2.VideoCapture(video_file)

    # Check if video file can be opened
    if not cap.isOpened():
        raise ValueError("Error opening video file")

    # Get the number of frames in the video
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize the Mediapipe Pose model
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Create a NumPy array to store the pose data
        num_landmarks = len(mp_pose.PoseLandmark)
        data = np.empty((3, num_landmarks, length))

        # Process each frame in the video
        frame_num = 0
        while cap.isOpened():
            ret, image = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            landmarks = results.pose_world_landmarks.landmark
            for i in range(num_landmarks):
                data[:, i, frame_num] = (landmarks[i].x, landmarks[i].y, landmarks[i].z)

            frame_num += 1

        # Release the video capture object
        cap.release()

    return data


def create_dataframe_from_data(data):
    frames = data.shape[2]
    landmark_indexes = np.arange(data.shape[1])
    num_landmarks = data.shape[1]

    columns = ['frame', 'row_id', 'type', 'landmark_index', 'x', 'y', 'z']

    
    df_list = []

    for frame in range(frames):
        for landmark_index in landmark_indexes:
            x, y, z = data[:, landmark_index, frame]
            row = [frame, f"{frame}-pose-{landmark_index}", 'pose', landmark_index, x, y, z]
            df_list.append(row)

    df = pd.DataFrame(df_list, columns=columns)
    return df




def process_videos_and_save_to_parquet(in_video_path = 'trimmed_mp4', out_parquet_path = 'landmarks', overwrite=False):
    if not os.path.exists(out_parquet_path):
        os.makedirs(out_parquet_path)

    video_files = [filename for filename in os.listdir(in_video_path) if filename.endswith(".mp4")]
    total_files = len(video_files)
    processed_files = 0

    for filename in video_files:
        video_file = os.path.join(in_video_path, filename)
        out_filename = filename.replace('.mp4', '')
        out_file = os.path.join(out_parquet_path, f"{out_filename}.parquet")

        if not overwrite and os.path.exists(out_file):
            print(f"Skipping {video_file} (Parquet file already exists)")
        else:
            try:
                print(f"Processing {video_file}...")
                data = create_data_from_video(video_file)
                df = create_dataframe_from_data(data)
                df.to_parquet(out_file)
                print(f"Data saved to {out_file}")
            except Exception as e:
                print(f"Error occurred while processing {video_file}: {str(e)}")
                continue

        processed_files += 1
        progress_percent = processed_files / total_files * 100
        print(f"Progress: {processed_files}/{total_files} ({progress_percent:.2f}%)")


if __name__ == "__main__":
  process_videos_and_save_to_parquet()