from pymongo import *

# 从 mongodb 获取格式化数据

client = MongoClient()
db = client['crop']
cropName = db['cropName']
data = db['data']
imgs = db['imgs']

for x in cropName.find():
    print(x)
for x in data.find():
    print(x)
for x in imgs.find():
    print(x)
