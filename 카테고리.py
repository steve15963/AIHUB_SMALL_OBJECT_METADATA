import json
import yaml

with open('trans_categories.json', 'r', encoding='utf-8') as file:
    jdata = json.load(file)

with open('yolov9-main/data/data.yaml', 'r', encoding='utf-8') as file:
    ydata = yaml.load(file, Loader=yaml.FullLoader)
ydata['names'] = []

for key,value in jdata.items():
    ydata['names'].append(value)

with open('yolov9-main/data/data.yaml','w') as file:
    yaml.dump(ydata,file)
    
print(ydata)
