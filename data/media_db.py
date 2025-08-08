import sqlite3
import os
import sys
from datetime import datetime

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS  # Temporary folder used by PyInstaller
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DB_PATH = os.path.join(get_base_dir(), "data", "media.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Ensure data/ exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_all_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM media_categories ORDER BY name")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def get_category_path(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM media_categories WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_category(name, path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO media_categories (name, path) VALUES (?, ?)", (name, path))
    conn.commit()
    conn.close()

def rename_category(old_name, new_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE media_categories SET name = ? WHERE name = ?", (new_name, old_name))
    conn.commit()
    conn.close()

def remove_category(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM media_categories WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def get_category_info():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, path, created_at FROM media_categories ORDER BY created_at DESC")
    results = cursor.fetchall()
    conn.close()
    return results
