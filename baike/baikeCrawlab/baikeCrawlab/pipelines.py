# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import shutil

import requests
import scrapy
from bson import binary
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy import Item
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings


class MongoTxtPipeline:
    def __init__(self):
        self.client = None
        self.db = None

    def open_spider(self, spider):
        self.client = MongoClient(get_project_settings().get('MONGODB_URI'))
        self.db = self.client[get_project_settings().get('MONGODB_DB_NAME')]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print('using txtPipeline...' + item['name'])
        path = os.getcwd()
        filepath = path + '/data/' + str(item['name'])
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
        filename = filepath + '/info.txt'
        # 把数据存到data文件夹
        with open(filename, 'w', encoding='utf-8') as f:
            for key, value in item.items():
                if type(value) is list:
                    for v in value:
                        f.write(v)
                elif type(value) is dict:
                    for k, v in value.items():
                        f.write(k + ':' + str(v) + '\n')
                else:
                    f.write(key + ':\n' + str(value) + '\n')
        f.close()
        # 数据在mongodb备份, 并且更新 cropsUrl
        self.insert_db(item)
        return item

    def insert_db(self, item):
        # 如果没出现, 向cropName插入遍历信息
        if self.db.cropName.count_documents({"name": item['name']}) == 0:
            print('mongoDB operating...')
            self.db.cropName.insert_one({'name': item['name'], 'url': item['url'], 'status': False})
            if isinstance(item, Item):
                item = dict(item)
                # 向集合data中插入文本数据
                self.db.data.insert_one(item)
        else:
            print('data already exists!')


# 在ImgPipeline的基础上连接数据库
class MongoImgPipeline(ImagesPipeline):
    client = None
    db = None
    img_store = None

    def open_spider(self, spider):
        print('spider opening...')
        self.client = MongoClient(get_project_settings().get('MONGODB_URI'))
        self.db = self.client[get_project_settings().get('MONGODB_DB_NAME')]
        self.img_store = get_project_settings().get('IMAGES_STORE')
        self.spiderinfo = self.SpiderInfo(spider)

    def close_spider(self, spider):
        self.client.close()
        print('spider closing...')

    # 发送图片下载请求
    def get_media_requests(self, item, info):
        src = item['src']
        print(src + '\nDownloading...')
        # 将图片被分在数据库里
        data = requests.get(src, timeout=10).content
        # 确认数据库中不存在此图片之后再保存在数据库imgs集合
        if not self.db.imgs.find_one({"src": src}):
            print('MongoDB IMG saving....')
            item["content"] = binary.Binary(data)
            itemDB = dict(item)
            self.db.imgs.insert_one(itemDB)
        # 在通过传统方式清求图片
        return scrapy.Request(url=src, meta={'plant_name': item['plant_name'], 'no': item['no']}, dont_filter=True)

    def file_path(self, request, response=None, info=None, *, item=None):
        print('file downloading...')
        if not os.path.exists(self.img_store):
            os.makedirs(self.img_store)
        name = "{}_{}.jpg".format(request.meta['plant_name'], request.meta['no'])
        return name

    # 将下载的文件保存到不同的目录中
    def item_completed(self, results, item, info):
        path = os.getcwd() + '/data/' + item['plant_name'] + '/' + item['name']
        # 目录不存在则创建目录
        if not os.path.exists(path):
            os.makedirs(path)
        img_name = '{}_{}.jpg'.format(item['plant_name'], item['no'])
        origin_name = '{}/{}_{}.jpg'.format(self.img_store, item['plant_name'], item['no'])
        # 将文件从默认下路路径移动到指定路径下
        try:
            shutil.move(origin_name, path)
            print('图片保存成功')
        except shutil.Error:
            print(path + '/' + img_name + " 已存在")
        except FileNotFoundError:
            print(origin_name + " 不存在")
        return item
