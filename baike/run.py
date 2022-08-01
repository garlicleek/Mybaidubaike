import os


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
    path = os.getcwd()
    spider_path = path + r'\baikeCrawlab'
    print("Now the project is woring at ", path)
    # 清空中间过程的cropsUrl文件
    with open(os.getcwd() + '/cropsUrl.txt', 'w') as f:
        f.write('')
    f.close()

    parm = {'spider': ['crops'], 'tag': r'{}\baikeCrawlab\baikeCrawlab\cropName.txt'.format(os.getcwd())}
    executeSpider(spider_path, parm)

    executeSelenium()

    parm['tag'] = r'{}\extendName.txt'.format(os.getcwd())

    executeSpider(spider_path, parm)
