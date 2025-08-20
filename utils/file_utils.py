import os

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)
