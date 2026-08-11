
import subprocess
from pathlib import Path
import os

def convert_to_480p(source, video_id):
    """Transcode the source video into a 480p HLS stream (playlist + segments)."""
    source_path = Path(source)
    path_name = source_path.parent / str(video_id) / "480p" / "index.m3u8"
    os.makedirs(path_name.parent, exist_ok=True)
    cmd = 'ffmpeg -i "{}" -s hd480 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}"'.format(source, path_name)
    subprocess.run(cmd, shell=True)

def convert_to_720p(source, video_id):
    """Transcode the source video into a 720p HLS stream (playlist + segments)."""
    source_path = Path(source)
    path_name = source_path.parent / str(video_id) / "720p" / "index.m3u8"
    os.makedirs(path_name.parent, exist_ok=True)
    cmd = 'ffmpeg -i "{}" -s hd720 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}"'.format(source, path_name)
    subprocess.run(cmd, shell=True)

def convert_to_1080p(source, video_id):
    """Transcode the source video into a 1080p HLS stream (playlist + segments)."""
    source_path = Path(source)
    path_name = source_path.parent / str(video_id) / "1080p" / "index.m3u8"
    os.makedirs(path_name.parent, exist_ok=True)
    cmd = 'ffmpeg -i "{}" -s hd1080 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}"'.format(source, path_name)
    subprocess.run(cmd, shell=True)


