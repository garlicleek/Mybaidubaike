import os

BOT_NAME = 'baikeCrawlab'
ITEM_PIPELINES = {'baikeCrawlab.pipelines.BaikespiderPipeline': 300}
NEWSPIDER_MODULE = 'baikeCrawlab.spiders'
ROBOTSTXT_OBEY = False
SPIDER_MODULES = ['baikeCrawlab.spiders']
IMAGES_STORE = os.getcwd() + '/imgTmp'
LOG_LEVEL = 'WARNING'
