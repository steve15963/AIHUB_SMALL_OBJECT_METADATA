import os
import shutil
from multiprocessing import Pool, cpu_count

# 소스 디렉토리 경로
source_directory = 'Z:\\037.Small object detection을 위한 이미지 데이터'

# 이미지와 JSON 파일을 복사할 대상 디렉토리 경로
image_destination = './train/image'
label_destination = './train/label'

# 대상 디렉토리 생성
os.makedirs(image_destination, exist_ok=True)
os.makedirs(label_destination, exist_ok=True)

# 이미지 파일 확장자 목록
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif')

def collect_files(directory):
    """
    디렉토리에서 모든 파일을 수집하여 경로와 목적지를 반환하는 함수
    """
    tasks = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(image_extensions):
                tasks.append((file_path, image_destination))
            elif file.lower().endswith('.json'):
                tasks.append((file_path, label_destination))
    return tasks

def copy_file(args):
    """
    파일을 지정된 목적지로 복사하는 함수
    """
    file_path, destination = args
    try:
        shutil.copy(file_path, destination)
        print(file_path)
        return f"{file_path} copied to {destination}"
    except Exception as e:
        return f"Error copying {file_path}: {e}"

if __name__ == '__main__':
    # 파일 경로와 목적지를 수집
    tasks = collect_files(source_directory)

    # 멀티프로세싱을 사용하여 파일 복사 작업 실행
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(copy_file, tasks)

    print("모든 파일 복사가 완료되었습니다.")

