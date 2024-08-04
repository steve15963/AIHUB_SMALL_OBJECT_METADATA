import json
import os
from sklearn.model_selection import train_test_split

def list_all_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext.lower() in image_extensions:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
    return file_paths

def save_file_list_to_txt(file_list, txt_file_path):
    with open(txt_file_path, 'w', encoding='utf-8') as file:
        for file_path in file_list:
            file.write(file_path + '\n')

cate = {}
image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
# JSON 파일을 탐색하여 class_id와 class_name을 추출 및 저장
file_list = list_all_files('Z:\\037.Small object detection을 위한 이미지 데이터\\01.데이터\\1.Training')

train_list, test_list = train_test_split(file_list, train_size=0.8,test_size=0.2,random_state=2000)

# file_list를 train.txt로 저장
save_file_list_to_txt(train_list, 'train.txt')
save_file_list_to_txt(test_list, 'test.txt')
