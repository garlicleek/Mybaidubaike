import cmd
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 用selenium获取星图中相关的关键词, 星图只取百科页面中的, 隐藏的星图暂未获取

path = os.getcwd()
par_path = os.path.dirname(path)
ChromePath = path + "/chromedriver.exe"

options = Options()
# options.add_argument('–-incognito')
# options.add_argument('--disable-infobars')
# options.add_argument('--start-maximized')
# options.add_argument('--headless')  # 设置chrome浏览器无界面模式

s = Service(ChromePath)
driver = webdriver.Chrome("chromedriver.exe", options=options)
# driver = webdriver.Chrome(options =options)
cropsUrl = []
# 实现去重
extendName = set()
urlList = []

print('开始执行selemium...')
with open(par_path + '/cropsUrl.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        cropsUrl.append(line.strip('\n'))
f.close()

for src in cropsUrl:
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
        print(nodes)
        for node in nodes:
            extendName.update(node.text)
        driver.implicitly_wait(5)  # seconds
        driver.back()
    print(extendName)

driver.quit()

# 把星图里面得到的关键词放入 extendName里, 由 coprs 爬虫进一步提取
with open(par_path + '/extendName.txt', 'w', encoding='utf-8') as f:
    for name in extendName:
        f.write(name + '\n')
f.close()
