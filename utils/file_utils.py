import os
import string
import subprocess
import sys
from config.media_config import video_extensions

def get_asset_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    if getattr(sys, 'frozen', False):  # Running as a bundled app
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def normalize(text):
    return ''.join(c for c in text if c not in string.whitespace + string.punctuation).lower()

def find_media_files(root_dir, media_title):
    matches = []
    title_norm = normalize(media_title)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if ext.lower() in video_extensions and title_norm in normalize(name):
                matches.append(os.path.join(dirpath, filename))
    return matches

def open_file(path):
    try:
        if sys.platform.startswith('win'):
            os.startfile(path)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', path])
        else:
            subprocess.run(['xdg-open', path])
    except Exception as e:
        print(f"Failed to open file: {e}")


