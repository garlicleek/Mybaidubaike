import os
import re

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from ..items import imgItem


class ImgSpider(scrapy.Spider):
    name = 'img'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/item/']
    custom_settings = {
            'ITEM_PIPELINES': {'baikeCrawlab.pipelines.MongoImgPipeline': 200}
        }
    crawlList = []
    offset = 0

    def start_requests(self):
        with open(os.path.dirname(os.getcwd()) + '/cropName.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.crawlList.append(self.start_urls[0] + line.strip('\n'))
        f.close()
        print(self.crawlList)
        yield Request(url=self.crawlList[0], callback=self.parse)

    def parse(self, response):
        # 去掉html标签的re模板
        # labelPattern = re.compile(r'<[^>]+>', re.S)

        # 判断是是多义词
        polysemous = response.xpath(
            "//div[@class='lemmaWgt-subLemmaListTitle']/following-sibling::ul[1]//a/@href").get()
        if polysemous is not None:
            url = "http://baike.baidu.com" + polysemous
            yield Request(url=url, callback=self.parse)

        else:
            soup = BeautifulSoup(response.text, 'lxml')

            # 词条名称
            title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
            item_name = title_node.get_text().strip()
            plant_name = item_name

            # 词条图册
            pictures_raw = response.xpath("//a[@class='more-link']/@href").get()
            pictures = "https://baike.baidu.com" + pictures_raw
            # 对于这个 url 通过selenium访问
            yield Request(url=pictures, callback=self.pictures_parse, meta={"plant_name": plant_name, "selenium": True})

        # 递归爬取下一个url
        if self.offset + 1 < len(self.crawlList):
            self.offset += 1
            yield Request(url=self.crawlList[self.offset])

    # 发现问题: 图片是动态加载的
    def pictures_parse(self, response):
        pictures_name = response.xpath('//a[@class="pic album-cover"]/@title').extract()
        for i in range(len(pictures_name)):
            pictures_url = response.xpath('(//div[@class="pic-list"])[{}]//img/@src'.format(str(i + 1))).extract()
            # print(pictures_name[i])
            # print(pictures_url)
            for j in range(len(pictures_url)):
                item = imgItem()
                item['plant_name'] = response.meta['plant_name']
                item['name'] = pictures_name[i]
                item['no'] = str(j)
                item['src'] = pictures_url[j]

                if item['src'][0] != 'h':
                    print('动态加载问题目前未解决')
                    print(response.url, item['src'])
                else:
                    print(item)
                    yield item
