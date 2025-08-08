from data.media_db import get_all_categories, get_category_path

# Optional: predefine the supported video extensions
video_extensions = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm"}

# Dynamically load media categories from the database
def load_media_dict():
    return {name: get_category_path(name) for name in get_all_categories()}
