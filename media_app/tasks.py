
import subprocess
from pathlib import Path

def convert_to_480p(source):
    source_path = Path(source)
    path_name = source_path.with_stem(f"{source_path.stem}_480p")

    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, path_name)
    subprocess.run(cmd, shell=True)


def convert_to_720p(source):
    source_path = Path(source)
    path_name = source_path.with_stem(f"{source_path.stem}_720p")

    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, path_name)
    subprocess.run(cmd, shell=True)