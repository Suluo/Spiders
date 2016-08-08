# Scrapy settings for dazong project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'dazong'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['dazong.spiders']
NEWSPIDER_MODULE = 'dazong.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = ['dazong.pipelines.DazongPipeline']
SCHEDULER_ORDER = 'BFO'
DEPTH_LIMIT = 10000
DOWNLOAD_DELAY = 3
