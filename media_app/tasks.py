
import subprocess
from pathlib import Path
import os

def convert_to_480p_hls_format(source):
    source_path = Path(source)
    path_name = source_path.with_stem(f"{source_path.stem}_480p")
    path_name = path_name.with_suffix('.m3u8')
    os.makedirs(path_name.parent, exist_ok=True)
    cmd = 'ffmpeg -i "{}" -s hd480 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}"'.format(source, path_name)
    subprocess.run(cmd, shell=True)


# def convert_to_720p(source):
#     source_path = Path(source)
#     path_name = source_path.with_stem(f"{source_path.stem}_720p")


#     cmd = 'ffmpeg  -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, path_name)
#     subprocess.run(cmd, shell=True)


