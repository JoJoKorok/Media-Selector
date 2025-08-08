# Media Selector
# Copyright (C) 2025  JoJoKorok
# Licensed under the GNU GPL v3 or later – see LICENSE file or https://www.gnu.org/licenses/

import tkinter as tk
import os
import sys
import random
from tkinter import ttk, messagebox, filedialog, simpledialog
from utils.path_utils import get_asset_path
from data.media_db import init_db
init_db()


from data.media_db import (
    get_all_categories,
    get_category_path,
    add_category,
    remove_category,
    rename_category,
)
from config.media_config import video_extensions
from utils.file_utils import find_media_files, open_file

# Suppress console window if run from a Windows shortcut or .bat file
if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

class MediaLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Launcher")
        self.root.geometry("600x550")

        self.media_type = tk.StringVar()
        self.search_term = tk.StringVar()
        self.results_map = {}

        self.set_background(get_asset_path("background.png"))  # PNG image only
        self.create_widgets()
        self.load_categories()

    def set_background(self, image_path):
        print(f"[DEBUG] Attempting to load background image from: {image_path}")
        if not os.path.exists(image_path):
            print("[DEBUG] Image path does not exist.")
            return
        try:
            self.bg_photo = tk.PhotoImage(file=image_path)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Failed to load background image:", e)


    def create_widgets(self):
        container = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        container.place(relx=0.5, rely=0.5, anchor='center', width=520, height=480)

        tk.Label(container, text="Select Media Type:", bg="#ffffff").pack(pady=(10, 0))
        self.media_dropdown = ttk.Combobox(container, textvariable=self.media_type, state="readonly")
        self.media_dropdown.pack(pady=5)

        btn_frame_top = tk.Frame(container, bg="#ffffff")
        btn_frame_top.pack(pady=5)
        tk.Button(btn_frame_top, text="+ Add Category", command=self.add_category_ui).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame_top, text="✎ Rename", command=self.rename_category_ui).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame_top, text="🗑 Remove", command=self.remove_category_ui).pack(side=tk.LEFT, padx=5)

        tk.Label(container, text="Search Title:", bg="#ffffff").pack(pady=(10, 0))
        tk.Entry(container, textvariable=self.search_term).pack(pady=5)
        tk.Button(container, text="Search", command=self.search_media).pack(pady=5)

        self.result_listbox = tk.Listbox(container, height=10, width=60)
        self.result_listbox.pack(pady=10)
        self.result_listbox.bind("<Double-1>", self.open_selected_file)

        btn_frame = tk.Frame(container, bg="#ffffff")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Pick Random Folder", command=self.pick_random).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Manual Browse", command=self.browse_manually).pack(side=tk.LEFT, padx=5)

    def load_categories(self):
        categories = get_all_categories()
        if not categories:
            self.media_dropdown["values"] = []
            self.media_type.set("")
        else:
            self.media_dropdown["values"] = categories
            if self.media_type.get() not in categories:
                self.media_type.set(categories[0])

    def search_media(self):
        self.result_listbox.delete(0, tk.END)
        self.results_map.clear()
        media_type = self.media_type.get()
        search_path = get_category_path(media_type)
        query = self.search_term.get().strip()

        if not query:
            messagebox.showwarning("Input Needed", "Please enter a search term.")
            return

        if not search_path or not os.path.isdir(search_path):
            messagebox.showerror("Invalid Path", "Selected media path is invalid or missing.")
            return

        results = find_media_files(search_path, query)
        if results:
            for path in results:
                filename = os.path.basename(path)
                self.result_listbox.insert(tk.END, filename)
                self.results_map[filename] = path
        else:
            messagebox.showinfo("No Results", "No matching files found.")

    def open_selected_file(self, event):
        selection = self.result_listbox.curselection()
        if not selection:
            return
        filename = self.result_listbox.get(selection[0])
        file_path = self.results_map.get(filename)
        if file_path:
            open_file(file_path)

    def pick_random(self):
        media_type = self.media_type.get()
        base_path = get_category_path(media_type)
        if not base_path or not os.path.isdir(base_path):
            messagebox.showerror("Error", "Invalid or missing directory for selected category.")
            return

        subfolders = [os.path.join(base_path, name) for name in os.listdir(base_path)
                      if os.path.isdir(os.path.join(base_path, name))]

        if not subfolders:
            messagebox.showinfo("No Subfolders", f"No subfolders found in '{base_path}'.")
            return

        selected_path = random.choice(subfolders)
        os.startfile(selected_path)

    def browse_manually(self):
        media_type = self.media_type.get()
        path = get_category_path(media_type)
        if path and os.path.isdir(path):
            os.startfile(path)
        else:
            messagebox.showerror("Error", "Invalid or missing directory for selected category.")

    def add_category_ui(self):
        category_name = simpledialog.askstring("New Category", "Enter category name:")
        if not category_name:
            return
        folder_path = filedialog.askdirectory(title="Select Folder for Category")
        if folder_path:
            try:
                add_category(category_name, folder_path)
                self.load_categories()
                self.media_type.set(category_name)
                messagebox.showinfo("Category Added", f"Category '{category_name}' has been added.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add category: {e}")

    def remove_category_ui(self):
        category = self.media_type.get()
        if not category:
            return
        confirm = messagebox.askyesno("Remove Category", f"Are you sure you want to remove '{category}'?")
        if confirm:
            try:
                remove_category(category)
                self.load_categories()
                messagebox.showinfo("Removed", f"Category '{category}' has been removed.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove category: {e}")

    def rename_category_ui(self):
        current = self.media_type.get()
        if not current:
            return
        new_name = simpledialog.askstring("Rename Category", f"Enter new name for '{current}':")
        if new_name and new_name != current:
            try:
                rename_category(current, new_name)
                self.load_categories()
                self.media_type.set(new_name)
                messagebox.showinfo("Renamed", f"'{current}' renamed to '{new_name}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename category: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaLauncherApp(root)
    root.mainloop()
