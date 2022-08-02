import os

from pymongo import *


def executeSpider(path, dic):
    # print('Executing: ' + path)
    for spider in dic['spider']:
        command1 = 'scrapy crawl {}'.format(spider)
        cd = "D: && cd " + path
        # cd = "cd " + path
        cmd = cd + ' && ' + command1
        print('Executing cmdline: ' + cmd)
        os.system(cmd)


def executeSelenium():
    command = 'python ./baikeSelenium/baikeSelenium.py'
    os.system(command)


if __name__ == '__main__':
    # 和获取每一部分的工作地址
    path = os.getcwd()
    spider_path = path + r'\baikeCrawlab'
    parm = {'spider': ['img']}
    print("Now the project is working at ", path)

    # 执行爬虫
    executeSpider(spider_path, parm)
    # 运行selenium
    # executeSelenium()
    # 再次运行爬虫
    # executeSpider(spider_path, parm)
