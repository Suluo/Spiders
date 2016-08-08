# Scrapy settings for douban project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'douban'
#BOT_VERSION = '1.0'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = ['douban.pipelines.MySQLStorePipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'douban (+http://www.douban.com)'
