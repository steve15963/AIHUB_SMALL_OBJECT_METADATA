import json
import os

from PIL import Image

def list_all_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

def loadfile(file_path):
    file, ext = os.path.splitext(file_path)
    if ext.lower() == '.json':
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {file_path}: {e}")
                return None
    else:
        return None

def save_to_text(data, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    width = data['images'][0]['width']
    height = data['images'][0]['height']
    

    annotations = data['annotations']

    name, ext = os.path.splitext(file_path)

    if width == 0 or height == 0:
        file_name_with_ext = os.path.basename(file_path)
        file_name, ext = os.path.splitext(file_name_with_ext)
        with Image.open(f'Z:\\valid\\images\\{file_name}.jpg') as img:
            width, height = img.size
    
    with open(name+'.txt','w',encoding='utf-8') as file:
        for annotation in annotations:
            categoryId = annotation['category_id'] - 1
            bbox = annotation['bbox']
            #print(name, width, height, bbox)
            #print(data)
            left_x = bbox[0] / width
            left_y = bbox[1] / height
            right_x = bbox[2] / width
            right_y = bbox[3] / height
            file.write(f"{categoryId} {left_x} {left_y} {right_x} {right_y}\n")

# JSON 파일을 탐색하여 class_id와 class_name을 추출 및 저장
file_list = list_all_files('Z:\\valid\\labels')
for path in file_list:
    data = loadfile(path)
    if data:
        save_to_text(data,path)
