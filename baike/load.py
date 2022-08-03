import os

from PIL import Image
from pymongo import *

# 从 mongodb 获取格式化数据
from urllib3.packages.six import BytesIO

client = MongoClient()
db = client['crop']
data = db['data']
imgs = db['imgs']

savePath = os.getcwd() + '/data'

# 保存 data 为 txt 文本
for x in db.data.find():
    path = savePath + '/' + x['name']
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + '/info.txt', 'w', encoding='utf-8') as f:
        for key, value in x.items():
            if type(value) is list:
                for v in value:
                    f.write(v)
            elif type(value) is dict:
                for k, v in value.items():
                    f.write(k + ':' + str(v) + '\n')
            else:
                f.write(key + ':\n' + str(value) + '\n')
# 保存imgs 为 jpg 图片
for img in imgs.find():
    path = savePath + '/' + img['plant_name'] + '/' + img['name']
    if not os.path.exists(path):
        os.makedirs(path)
    filename = path + '/' + img['no'] + '.jpg'
    with open(filename, 'wb') as f:
        f.write(img['content'])
