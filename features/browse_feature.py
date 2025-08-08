import os
import sys
from utils.file_utils import find_media_files, open_file
from utils.prompt_utils import prompt_continue
from config.media_config import video_extensions
from data.media_db import get_all_categories, get_category_path

def browse_categories():
    while True:
        categories = get_all_categories()
        if not categories:
            print("No media categories found. Add some first.")
            return

        print("\nAvailable Media Categories:")
        for i, name in enumerate(categories, 1):
            print(f"{i}. {name}")
        print("[0] Cancel")

        try:
            choice = input("Select a category to browse: ").strip()
            if choice == '0':
                return
            index = int(choice) - 1
            if 0 <= index < len(categories):
                selected = categories[index]
                path = get_category_path(selected)
                if path and os.path.isdir(path):
                    browse_path(path)
                else:
                    print("Invalid or inaccessible path.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")

def browse_path(start_path):
    current_path = start_path
    history = []

    while True:
        try:
            entries = sorted(os.listdir(current_path))
        except PermissionError:
            print("Cannot access this folder.")
            if history:
                current_path = history.pop()
            else:
                return

        subdirs = [d for d in entries if os.path.isdir(os.path.join(current_path, d))]
        videos = [f for f in entries if os.path.isfile(os.path.join(current_path, f)) and os.path.splitext(f)[1].lower() in video_extensions]

        print(f"\nBrowsing: {current_path}")
        print("\nFolders:")
        for i, d in enumerate(subdirs, 1):
            print(f"{i}. {d}/")

        print("\nVideo Files:")
        for i, f in enumerate(videos, len(subdirs) + 1):
            print(f"{i}. {f}")

        print("\nOptions:")
        print("[0] Go back")
        print("[C] Return to category selection")
        print("[S] Search this folder")

        choice = input("Enter number to open folder/file, [S] to search, or [C]/0 to go back: ").strip().lower()

        if choice == '0':
            if history:
                current_path = history.pop()
            else:
                return

        elif choice == 'c':
            return  # back to category selection

        elif choice == 's':
            search_term = input("Enter title to search for in this folder and its subfolders: ").strip()
            results = find_media_files(current_path, search_term)

            if results:
                print(f"\nFound {len(results)} result(s):")
                for idx, path in enumerate(results, 1):
                    print(f"{idx}. {path}")
                while True:
                    try:
                        sel = int(input("Enter number to open (0 to cancel): "))
                        if sel == 0:
                            break
                        selected = results[sel - 1]
                        print(f"\nOpening: {selected}")
                        open_file(selected)
                        if not prompt_continue():
                            sys.exit()
                        return
                    except (ValueError, IndexError):
                        print("Invalid selection. Try again.")
            else:
                print("No matching media files found.")

        else:
            try:
                idx = int(choice) - 1
                if idx < len(subdirs):
                    history.append(current_path)
                    current_path = os.path.join(current_path, subdirs[idx])
                else:
                    file_path = os.path.join(current_path, videos[idx - len(subdirs)])
                    print(f"\nOpening: {file_path}")
                    open_file(file_path)
                    if not prompt_continue():
                        sys.exit()
                    return
            except (ValueError, IndexError):
                print("Invalid input. Try again.")
