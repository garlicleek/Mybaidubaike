import cmd
import os
import time
from pymongo import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 用selenium获取星图中相关的关键词, 星图只取百科页面中的, 隐藏的星图暂未获取

# 连接浏览器
path = os.getcwd()
ChromePath = path + "/baikeSelenium/chromedriver.exe"
print(ChromePath)
options = Options()
# options.add_argument('–-incognito')
# options.add_argument('--disable-infobars')
# options.add_argument('--start-maximized')
options.add_argument('--headless')  # 设置chrome浏览器无界面模式

s = Service(ChromePath)
driver = webdriver.Chrome(ChromePath, options=options)
# driver = webdriver.Chrome(options =options)
cropsUrl = []
# 连接数据库
extendName = []
urlList = []
client = MongoClient()
db = client['crop']

# 遍历每一个为 False 的元素
print('开始执行selemium...')
for x in db.cropName.find({'status': False}):
    cropsUrl.append(x['url'])
# for x in db.cropName.find():
#     cropsUrl.append(x['url'])

for src in cropsUrl:
    # 更新为 True
    # db.cropName.update_one({'url': src}, {'$set': {'status': True}})
    # 进入selenium
    print('正在进入', src)
    driver.get(src)
    starElements = driver.find_elements(by=By.CLASS_NAME, value='starmap-theme-title')
    for starElement in starElements:
        # 进入每一个分支的星图
        urlList.append(starElement.get_attribute('href'))
    print('已获取星图url...')

    for url in urlList:
        print('正在进入星图页面...', url)
        driver.get(url)
        driver.implicitly_wait(5)  # seconds
        # print(driver.page_source)
        print('已进入星图')
        nodes = driver.find_elements(by=By.CSS_SELECTOR, value='a.sc-cTQhss.sc-dPyBCJ.fSATAG.cDOhpo')

        for node in nodes:
            if node.text not in extendName:
                extendName.append(node.text)
        driver.implicitly_wait(5)  # seconds
        driver.back()

driver.quit()

# 把星图里面得到的关键词放入 cropName里, 由爬虫进一步提取
with open(path + '/cropName.txt', 'w', encoding='utf-8') as f:
    for name in extendName:
        f.write(name + '\n')
f.close()
