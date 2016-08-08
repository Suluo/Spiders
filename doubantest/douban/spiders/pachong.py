# -*- coding: UTF-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from douban.items import DoubanItem
 
class douban(BaseSpider):
    name = "pachong"
    allow_domains = ["http://book.douban.com/tag/编程?type=S"]
    start_urls = ["http://book.douban.com/tag/编程?type=S"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        item = DoubanItem()
        item['title'] = hxs.select('//ul/li[position()>0]/div[2]/h2/a/@title').extract()
        item['link'] = hxs.select('//ul/li[position()>0]/div[2]/h2/a/@href').extract() 
        items.append(item)
        return items


