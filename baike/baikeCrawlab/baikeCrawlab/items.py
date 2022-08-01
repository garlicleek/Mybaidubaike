# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaikespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    basicInfo = scrapy.Field()
    paragraph = scrapy.Field()


class imgItem(scrapy.Item):
    src = scrapy.Field()
    name = scrapy.Field()
    plant_name = scrapy.Field()
    no = scrapy.Field()
