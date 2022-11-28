from dataclasses import replace
from pathlib import Path
import sys
import os

def sorting(dir=None):
    if dir is None:
        dir = sys.argv[1]
    images_path = dir + "images"
    videos_path = dir + "videos"
    docs_path = dir + "docs"
    musics_path = dir + "musics"
    zips_path = dir + "zips"
    not_recognize_path = dir + "not_recognize"

    if not os.path.exists(images_path):
        os.makedirs(images_path)
    if not os.path.exists(videos_path):
        os.makedirs(videos_path)
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
    if not os.path.exists(musics_path):
        os.makedirs(musics_path)
    if not os.path.exists(zips_path):
        os.makedirs(zips_path)
    if not os.path.exists(not_recognize_path):
        os.makedirs(not_recognize_path)
    
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if file_path.endswith(('.jpg', '.png', '.png', '.svg', '.jfif', '.gif')):
            new_file = os.path.join(images_path, file)
            os.replace(file_path, new_file)
        elif file_path.endswith(('.avi', '.mp4', '.mov', '.mkv')):
            new_file = os.path.join(videos_path, file)
            os.replace(file_path, new_file)
        elif file_path.endswith(('.doc', '.docx', '.txt', '.pdf', '.xlxs', '.pptx')):
            new_file = os.path.join(docs_path, file)
            os.replace(file_path, new_file)
        elif file_path.endswith(('.mp3', '.ogg', '.wav', '.amr')):
            new_file = os.path.join(musics_path, file)
            os.replace(file_path, new_file)
        elif file_path.endswith(('.zip', '.gz', '.tar')):
            new_file = os.path.join(zips_path, file)
            os.replace(file_path, new_file)
        elif os.path.isfile(dir + file):
            new_file = os.path.join(not_recognize_path, file)
            os.replace(file_path, new_file)