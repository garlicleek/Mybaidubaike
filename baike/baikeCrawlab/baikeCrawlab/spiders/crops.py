import os
import re

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
from ..items import BaikespiderItem
from multiprocessing import Process


class CropsSpider(scrapy.Spider):
    name = 'crops'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/item/']
    crawlList = []
    custom_settings = {
        'ITEM_PIPELINES': {'baikeCrawlab.pipelines.MongoTxtPipeline': 300}
    }
    offset = 0

    def start_requests(self):
        # windows 和 Linux 的寻址方式不同, 所以推荐使用绝对路径
        with open(os.path.dirname(os.getcwd()) + '/cropName.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.crawlList.append(self.start_urls[0] + line.strip('\n'))
        f.close()
        #
        print(self.crawlList)
        yield Request(url=self.crawlList[0], dont_filter=True)

    def parse(self, response):
        # 去掉html标签的re模板
        # labelPattern = re.compile(r'<[^>]+>', re.S)

        # 判断是是多义词
        polysemous = response.xpath(
            "//div[@class='lemmaWgt-subLemmaListTitle']/following-sibling::ul[1]//a/@href").get()
        if polysemous is not None:
            url = "http://baike.baidu.com" + polysemous
            yield Request(url=url)

        else:
            soup = BeautifulSoup(response.text, 'lxml')

            item = BaikespiderItem()
            # 去除注释
            regex = re.compile('\[.{0,7}\]')
            # url
            item['url'] = response.url
            # 名称
            item_name = ''
            try:
                title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
                item_name = title_node.get_text().strip()
                item['name'] = item_name
            except AttributeError:
                item['name'] = ''
                print(response.url, 'name 不存在')

            # 描述
            summary_node = soup.find('div', class_='lemma-summary')
            try:
                text = regex.sub('', summary_node.get_text().strip()).replace('\n', '').strip()
                item['description'] = text
            except AttributeError:
                item['description'] = ''
                print(response.url, 'description 不存在')

            # 基本信息
            try:
                basic_name = soup.findAll('dt', class_='basicInfo-item name')
                basic_value = soup.findAll('dd', class_='basicInfo-item value')
                basic = {}
                for i in range(len(basic_name)):
                    name = str(basic_name[i].get_text()).replace('\xa0', '').strip() + '：'
                    value = str(basic_value[i].get_text()).replace('\xa0', '').strip()
                    # 去掉[1][12-13]这样的注释
                    value = regex.sub('', value).strip()
                    basic.update({name: value})
                item['basicInfo'] = basic
            except AttributeError:
                item['basicInfo'] = ''
                print(response.url, 'basicInfo 不存在')

            # 去除图片中的文字
            tags = soup.findAll('div', class_='lemma-picture text-pic layout-right')
            for tag in tags:
                tag.clear()
            # 去掉前面的描述，防止对解析后面的文字造成干扰
            summary_node.clear()
            # 大段的描述
            paras = soup.findAll('div', class_='para')
            # 遍历para标签，寻找上一个h2标签作为属性名，h2之间的文字作为属性值
            try:
                para = ''
                temp_h2 = paras[0].find_previous('h2').get_text().replace(item_name, '')
                temp_para = ''
                para += temp_h2 + ':'
                for i in range(len(paras)):
                    text = paras[i].get_text()
                    text = regex.sub('', text).strip().replace('\n', '')
                    h2 = paras[i].find_previous('h2').get_text().replace(item_name, '')
                    if h2 == temp_h2:
                        temp_para += text
                    else:
                        para += temp_para
                        para += '\n' + h2 + ':'
                        temp_para = text
                        temp_h2 = h2
                    if i == len(paras) - 1:
                        para += temp_para
                item['paragraph'] = para
            except AttributeError:
                item['paragraph'] = ''
                print(response.url, 'para 不存在')
            print(item)
            yield item

        # 递归爬取下一个url
        if self.offset + 1 < len(self.crawlList):
            self.offset += 1
            yield Request(url=self.crawlList[self.offset], dont_filter=True)
