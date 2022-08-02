import os

# 爬虫基本信息
BOT_NAME = 'baikeCrawlab'
NEWSPIDER_MODULE = 'baikeCrawlab.spiders'
ROBOTSTXT_OBEY = False
SPIDER_MODULES = ['baikeCrawlab.spiders']
ITEM_PIPLINES = {
    'baikeCrawlab.pipelines.MongoTxtPipeline': 300
}
DOWNLOADER_MIDDLEWARES = {
    'baikeCrawlab.middlewares.CropsDownloaderMiddleware': 200
}

# mongoDB的连接参数
MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DB_NAME = 'crop'
# 图片存储路径
IMAGES_STORE = os.getcwd() + '/imgTmp'
# 日志等级
LOG_LEVEL = 'WARNING'
