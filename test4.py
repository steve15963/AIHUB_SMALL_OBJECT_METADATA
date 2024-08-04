from glob import glob

from sklearn.model_selection import train_test_split

import yaml

def list_all_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

img_list = list_all_files('Z:\\037.Small object detection을 위한 이미지 데이터\\01.데이터\\2.Validation')

print(len(img_list))

train_list, test_list = train_test_split(img_list, train_size=0.8,test_size=0.2,random_state=2000)

vaild_list = glob('data/valid/images/*.jpg')

print(len(img_list))
print(len(train_list))
print(len(test_list))
print(len(vaild_list))

with open('data/train.txt','w') as file:
    file.write('\n'.join(train_list)+'\n')

with open('data/test.txt','w') as file:
    file.write('\n'.join(test_list)+'\n')

with open('data/vaild.txt','w') as file:
    file.write('\n'.join(vaild_list)+'\n')

with open('data/data.yaml','r') as file:
    data = yaml.load(file,Loader=yaml.FullLoader)

data['train'] = './data/train.txt'
data['val'] = './data/vaild.txt'
data['test'] = './data/test.txt'

with open('data/data.yaml','w') as file:
    yaml.dump(data,file)
