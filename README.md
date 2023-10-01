# 3DYoga90
![Screen Shot 2023-10-02 at 6.25.05 AM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/39e7032a-9f2a-403d-83b4-3a3ee8d34644/a3728ae3-d004-441f-bcc1-00720e394aa3/Screen_Shot_2023-10-02_at_6.25.05_AM.png)

This repo is the official repo of 3DYoga90 dataset. If you want to download original videos and sequences, follow the steps below. 

![Screen Shot 2023-10-02 at 6.25.36 AM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/39e7032a-9f2a-403d-83b4-3a3ee8d34644/a647bf06-ac2a-406e-a99a-c059ddba733b/Screen_Shot_2023-10-02_at_6.25.36_AM.png)

Step 1. Download raw videos.

```

cd data_process
python video_downloader.py

```

Step 2. Extract sequences from raw videos using [3DYoga90.json](https://github.com/seonokkim/3DYoga90/blob/main/data/3DYoga90.json).

```
python preprocess.py

```

Step 2. Generate skeleton files from the sequences.

```
python skeleton_generator.py

```

 If you want to download the skeleton dataset of sequences, download files from [google drive](https://drive.google.com/drive/folders/11SOWVJ5CF5pbkftMqogVP5Pkyg88hbau?usp=sharing). The dataset structure is inspired by [Google - Isolated Sign Language Recognition](https://www.kaggle.com/competitions/asl-signs/data?select=train_landmark_files).
