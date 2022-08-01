import os

from pymongo import *


def executeSpider(path, dic):
    print('Executing: ' + path)

    for spider in dic['spider']:
        command1 = 'scrapy crawl {} -a tag={}'.format(spider, dic['tag'])
        cd = "D: && cd " + path
        # cd = "cd " + path
        cmd = cd + ' && ' + command1
        # print('cmd: ' + cmd)
        os.system(cmd)


def executeSelenium():
    command = 'python ./baikeSelenium/baikeSelenium.py'
    os.system(command)


if __name__ == '__main__':
    # 和获取每一部分的工作地址
    path = os.getcwd()
    spider_path = path + r'\baikeCrawlab'
    print("Now the project is working at ", path)


    # 执行爬虫

    # 运行selenium

    # 再次运行爬虫

    # 以下代码是通过文件传输的代码, 已弃用
    # parm = {'spider': ['crops'], 'tag': r'{}\baikeCrawlab\baikeCrawlab\cropName.txt'.format(os.getcwd())}
    # executeSpider(spider_path, parm)
    # executeSelenium()
    # parm['tag'] = r'{}\extendName.txt'.format(os.getcwd())
    #
    # executeSpider(spider_path, parm)
