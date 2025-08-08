'''
This is the default added catagories for me when I initially made this little program.
'''

from data.media_db import add_category

default_categories = {
    "Movies": "E:\\Movies",
    "Live Action Shows": "D:\\TV and Web Shows\\Live Action Television Shows",
    "Anime": "D:\\TV and Web Shows\\Anime",
    "Cartoons": "D:\\TV and Web Shows\\Cartoons",
    "3D Shows": "D:\\TV and Web Shows\\3D Shows",
    "Web Shows": "D:\\TV and Web Shows\\Web Shows"
}

for name, path in default_categories.items():
    add_category(name, path)

print("Default categories have been added.")
