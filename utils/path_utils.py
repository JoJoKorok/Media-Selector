import os
import sys

def get_asset_path(filename, subfolder="assets"):
    if getattr(sys, 'frozen', False):
        # PyInstaller onefile extracts to temp folder
        base_path = sys._MEIPASS
    else:
        # Running from source
        base_path = os.path.join(os.path.dirname(__file__), "..", subfolder)
        return os.path.abspath(os.path.join(base_path, filename))
    return os.path.join(base_path, subfolder, filename)
