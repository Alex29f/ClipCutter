# Video Cutter Script (Batch Processing with Multi-threading)

Made this script because I had bunch of ~2min clips where only in the last 15 seconds something happens, and those files are too big if you want to share them with friends.

This script allows users to cut the last **N** seconds from all video files in a directory. It uses **multi-threading (6 threads)** to process multiple video files in parallel and outputs the modified files with the desired bitrate and framerate. 

In the releases section, there will be a pre-compiled `.exe` file, so you can simply drop it into the directory containing your video files. The script will cut the last **N** seconds as specified by the user from all files in that directory.



## Features
- Batch process all video files in a directory
- Cut the last **N** seconds from each video file
- Multi-threading support (6 threads)
- Customize output bitrate and framerate

## Requirements

If you are using the Python script version, make sure you have:

- Python 3.x
- [ffmpeg](https://ffmpeg.org/download.html)
