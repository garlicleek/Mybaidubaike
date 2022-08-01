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
        # 向cropName插入遍历信息
        self.db.cropName.insert({'name': item['name'], 'url': item['url'], 'status': True})
        if isinstance(item, Item):
            item = dict(item)  # 将一项数据转化为字典格式
        # 如果数据库没有数据,向集合data中插入文本数据
        if not self.db.data.find_one({"name": item['name']}):
            self.db.books.insert_one(item)


# 在ImgPipeline的基础上连接数据库
class MongoImgPipeline:
    def __init__(self):
        self.client = None
        self.db = None
        self.img_store = None

    def open_spider(self, spider):
        self.client = MongoClient(get_project_settings().get('MONGODB_URI'))
        self.db = self.client[get_project_settings().get('MONGODB_DB_NAME')]
        self.img_store = get_project_settings().get('IMAGES_STORE')

    def close_spider(self, spider):
        self.client.close()

    # 发送图片下载请求
    def get_media_requests(self, item, info):
        src = item['src']
        print(src + '\nDownloading...')
        # 将图片被分在数据库里
        data = requests.get(src, timeout=10).content
        # 确认数据库中不存在此图片之后再保存在数据库imgs集合
        if not self.db.imgs.find_one({"src": src}):
            item["content"] = binary.Binary(data)
            self.db.imgs.insert_one(item)
        # 在通过传统方式清求图片
        return scrapy.Request(url=src, meta={'plant_name': item['plant_name'], 'no': item['no']}, dont_filter=True)

    def file_path(self, request, response=None, info=None, *, item=None):
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
        except shutil.Error:
            print(path + '/' + img_name + " 已存在")
        except FileNotFoundError:
            print(origin_name + " 不存在")
        return item


# BaikespiderPipeline 是通过txt传输数据的. 已弃用
# class BaikespiderPipeline:
#     def process_item(self, item, spider):
#         print('using txtPipeline...' + item['name'])
#                 path = os.getcwd()
#                 filepath = path + '/data/' + str(item['name'])
#                 if not os.path.isdir(filepath):
#                     os.makedirs(filepath)
#                 filename = filepath + '/info.txt'
#                 # 把数据存到data文件夹
#                 with open(filename, 'w', encoding='utf-8') as f:
#                     for key, value in item.items():
#                         if type(value) is list:
#                             for v in value:
#                                 f.write(v)
#                         elif type(value) is dict:
#                             for k, v in value.items():
#                                 f.write(k + ':' + str(v) + '\n')
#                         else:
#                             f.write(key + ':\n' + str(value) + '\n')
#                 f.close()
#         # 把 url 存到 coprsUrl.txt 文件夹用来进行星图的selenium爬虫, 储存到和爬虫文件同级
#         parent_path = os.path.dirname(path)
#         with open(parent_path + '/cropsUrl.txt', 'a', encoding='utf-8') as f:
#             f.write(item['url'] + '\n')
#         f.close()
#
#         return item


# 本图片管道是用来下载图片到本地的. 已弃用
# class ImgsPipeline(ImagesPipeline):
#     # 从项目设置文件中导入图片下载路径
#     img_store = get_project_settings().get('IMAGES_STORE')
#
#     # 发送图片下载请求
#     def get_media_requests(self, item, info):
#         src = item['src']
#         print(src + '\nDownloading...')
#         return scrapy.Request(url=src, meta={'plant_name': item['plant_name'], 'no': item['no']}, dont_filter=True)
#
#     def file_path(self, request, response=None, info=None, *, item=None):
#         if not os.path.exists(self.img_store):
#             os.makedirs(self.img_store)
#         name = "{}_{}.jpg".format(request.meta['plant_name'], request.meta['no'])
#         return name
#
#     # 重写item_completed方法
#     # 将下载的文件保存到不同的目录中
#     def item_completed(self, results, item, info):
#         path = os.getcwd() + '/data/' + item['plant_name'] + '/' + item['name']
#
#         # 目录不存在则创建目录
#         if not os.path.exists(path):
#             os.makedirs(path)
#
#         img_name = '{}_{}.jpg'.format(item['plant_name'], item['no'])
#         origin_name = '{}/{}_{}.jpg'.format(self.img_store, item['plant_name'], item['no'])
#
#         # 将文件从默认下路路径移动到指定路径下
#         try:
#             shutil.move(origin_name, path)
#         except shutil.Error:
#             print(path + '/' + img_name + " 已存在")
#         except FileNotFoundError:
#             print(origin_name + " 不存在")
#         # print(path)
#
#         return item
