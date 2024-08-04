import os
import shutil
import multiprocessing
from multiprocessing import Pool

def list_all_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

def copy_file(file_path):
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    json_extension = '.json'

    file, ext = os.path.splitext(file_path)
    
    print(file)
    if ext.lower() in image_extensions:
        dest_folder = './train/images'
    elif ext.lower() == json_extension:
        dest_folder = './train/label'
    else:
        return  # 파일이 이미지 또는 JSON 파일이 아닌 경우 처리하지 않음

    os.makedirs(dest_folder, exist_ok=True)
    shutil.copy(file_path, dest_folder)

def distribute_files(files, num_processes):
    chunk_size = len(files) // num_processes
    chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    # 나머지 파일들을 마지막 청크에 추가
    for i in range(len(files) % num_processes):
        chunks[i].append(files[num_processes * chunk_size + i])

    with Pool(processes=num_processes) as pool:
        pool.map(copy_file, files)

def main(source_directory):
    all_files = list_all_files(source_directory)
    num_cpus = multiprocessing.cpu_count()

    distribute_files(all_files, num_cpus)

if __name__ == '__main__':
    source_directory = 'Z:\\037.Small object detection을 위한 이미지 데이터\\01.데이터\\1.Training'   # 여기에 대상 디렉토리 경로를 설정하세요.
    main(source_directory)
