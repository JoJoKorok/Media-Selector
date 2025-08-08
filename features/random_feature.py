import os
import random
from data.media_db import get_all_categories, get_category_path

def get_random_subfolder_path():
    while True:
        categories = get_all_categories()
        if not categories:
            print("No media categories found in the database.")
            return None

        print("\nAvailable media types:")
        for name in categories:
            print(f"- {name}")
        user_input = input("\nWhat would you like randomly selected from? Enter type exactly as shown (or 'q' to cancel): ").strip()
        if user_input.lower() == 'q':
            return None

        if user_input not in categories:
            print("\nInvalid selection. Please try again.\n")
            continue

        parent_folder_path = get_category_path(user_input)
        if not parent_folder_path or not os.path.isdir(parent_folder_path):
            print(f"\nError: '{parent_folder_path}' is not a valid directory.")
            return None
        break

    subfolders = [
        d for d in os.listdir(parent_folder_path)
        if os.path.isdir(os.path.join(parent_folder_path, d))
    ]

    if not subfolders:
        print(f"\nNo subfolders found in '{parent_folder_path}'.")
        return None

    random_subfolder = random.choice(subfolders)
    selected_path = os.path.join(parent_folder_path, random_subfolder)
    print(f"\nRandomly selected: {random_subfolder}")
    return selected_path
