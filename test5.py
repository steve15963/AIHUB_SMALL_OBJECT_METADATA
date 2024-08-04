import json
import os

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

def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

cate = {}

# JSON 파일을 탐색하여 class_id와 class_name을 추출 및 저장
file_list = list_all_files('Z:\\037.Small object detection을 위한 이미지 데이터\\01.데이터\\2.Validation')
for path in file_list:
    data = loadfile(path)
    if data is not None:
        objs = data.get('categories', [])
        for obj in objs:
            print(obj['class_name'])
            cate[obj['class_id']] = obj['class_name']

# cate 딕셔너리를 키로 정렬
sorted_cate = dict(sorted(cate.items()))

print(sorted_cate)
# 결과를 JSON 파일로 저장
output_file_path = 'sorted_categories.json'
save_to_json(sorted_cate, output_file_path)

print(f"Sorted categories have been saved to {output_file_path}.")
