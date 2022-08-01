# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import shutil

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings


class BaikespiderPipeline:
    def process_item(self, item, spider):
        print('using txtPipeline...' + item['name'])
        path = os.getcwd()
        filepath = path + '/data/' + str(item['name'])
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
        filename = filepath + '/info.txt'
        # print(filename)

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

        # 把 url 存到 coprsUrl.txt 文件夹用来进行星图的selenium爬虫, 储存到和爬虫文件同级
        parent_path = os.path.dirname(path)
        with open(parent_path + '/cropsUrl.txt', 'a', encoding='utf-8') as f:
            f.write(item['url'] + '\n')
        f.close()

        return item


# 图片管道
class ImgsPipeline(ImagesPipeline):
    # 从项目设置文件中导入图片下载路径
    img_store = get_project_settings().get('IMAGES_STORE')

    # 发送图片下载请求
    def get_media_requests(self, item, info):
        src = item['src']
        print(src + '\nDownloading...')
        return scrapy.Request(url=src, meta={'plant_name': item['plant_name'], 'no': item['no']}, dont_filter=True)

    def file_path(self, request, response=None, info=None, *, item=None):
        if not os.path.exists(self.img_store):
            os.makedirs(self.img_store)
        name = "{}_{}.jpg".format(request.meta['plant_name'], request.meta['no'])
        return name

    # 重写item_completed方法
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
            print(path+'/'+img_name + " 已存在")
        except FileNotFoundError:
            print(origin_name + " 不存在")
        # print(path)

        return item
