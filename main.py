# Media Selector
# Copyright (C) 2025  JoJoKorok
# Licensed under the GNU GPL v3 or later – see LICENSE file or https://www.gnu.org/licenses/

import os
import sys
from features.random_feature import get_random_subfolder_path
from features.browse_feature import browse_categories
from data.media_db import get_all_categories, get_category_path, add_category
from utils.file_utils import find_media_files, open_file
from utils.prompt_utils import prompt_continue

def ensure_categories_exist():
    categories = get_all_categories()
    while not categories:
        print("\nNo media categories found.")
        choice = input("Would you like to add one now? [Y/n]: ").strip().lower()
        if choice == 'n':
            print("Cannot continue without categories. Exiting.")
            sys.exit()
        name = input("Enter a name for this media category: ").strip()
        path = input("Enter the full path to the folder for this category: ").strip()
        if os.path.isdir(path):
            add_category(name, path)
            print(f"Category '{name}' added.")
            categories = get_all_categories()
        else:
            print("That path does not exist or is not a directory. Please try again.")
    return categories

def main():
    while True:
        print("\n==== Media Launcher ====")
        print("[1] Search for a specific title")
        print("[2] Pick a random subfolder to browse")
        print("[3] Exit")

        first_choice = input("> ").strip()

        if first_choice == '1':
            pass  # fall through to search below
        elif first_choice == '2':
            selected_path = get_random_subfolder_path()
            if selected_path:
                browse_categories()
            continue
        elif first_choice == '3':
            print("Exiting.")
            return
        else:
            print("Invalid input. Please choose 1, 2, or 3.")
            continue

        categories = ensure_categories_exist()

        print("\nAvailable media types:")
        for key in categories:
            print(f"- {key}")

        media_type_input = input("\nEnter the type of media (or 'q' to quit): ").strip().lower()
        if media_type_input == 'q':
            print("Exiting.")
            break

        media_type = next((key for key in categories if key.lower() == media_type_input), None)
        if media_type is None:
            print("Invalid media type. Please try again.")
            continue

        search_path = get_category_path(media_type)
        if not search_path or not os.path.isdir(search_path):
            print("Invalid path for selected category.")
            continue

        while True:
            media_title = input("Enter the title of the media you're looking for: ").strip()
            print(f"\nSearching in: {search_path}...\n")
            results = find_media_files(search_path, media_title)

            if results:
                print(f"Found {len(results)} result(s):\n")
                for idx, file in enumerate(results, 1):
                    print(f"{idx}. {file}")
                while True:
                    try:
                        choice = int(input("\nEnter the number of the file you want to open (0 to cancel): "))
                        if choice == 0:
                            print("Operation cancelled.")
                            break
                        selected_file = results[choice - 1]
                        print(f"\nOpening: {selected_file}")
                        open_file(selected_file)
                        if not prompt_continue():
                            return
                        break
                    except (ValueError, IndexError):
                        print("Invalid selection. Please try again.")
                break
            else:
                print("No matching media files found.")
                while True:
                    fallback = input(
                        "\nWhat would you like to do?\n"
                        "[1] Search again\n"
                        "[2] Browse folders manually\n"
                        "[3] Cancel\n> ").strip()
                    if fallback == '1':
                        break
                    elif fallback == '2':
                        browse_categories()
                        break
                    elif fallback == '3':
                        break
                    else:
                        print("Invalid input. Please enter 1, 2, or 3.")
                break

if __name__ == "__main__":
    main()
