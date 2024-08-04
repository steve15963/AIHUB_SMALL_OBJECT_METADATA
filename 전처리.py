from glob import glob

from sklearn.model_selection import train_test_split

import yaml

img_list = glob('train/images/*.jpg')

print(len(img_list))

train_list, test_list = train_test_split(img_list, train_size=0.8,test_size=0.2,random_state=2000)

valid_list = glob('valid/images/*.jpg')

print(len(img_list))
print(len(train_list))
print(len(test_list))
print(len(valid_list))

with open('data/train.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(train_list) + '\n')

with open('data/test.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(test_list) + '\n')

with open('data/valid.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(valid_list) + '\n')

# with open('data/data.yaml','r') as file:
#     data = yaml.load(file,Loader=yaml.FullLoader)

# data['train'] = './data/train.txt'
# data['val'] = './data/vaild.txt'
# data['test'] = './data/test.txt'

# with open('data/data.yaml','w') as file:
#     yaml.dump(data,file)
