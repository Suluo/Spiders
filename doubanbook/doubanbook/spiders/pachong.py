#!/usr/bin/env python
# -*- coding:utf-8 -*-
#############################################
# Description:
# File Name: pachong.py
# Author:Suluo-Sampson.suluo@gmail.com
# Last modified: 2016-07-20 20:35:15
# Python Release:2.7
###############################################
import logging
import logging.handlers
import logging.config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from doubanbook.items import DoubanbookItem
from scrapy.http import Request


class doubanbookSpider(BaseSpider):
    name = 'pachong'
    allow_domains = ['http://book.douban.com']
    start_urls = ['http://book.douban.com/tag/编程?start=0&type=S']

    def __init__(self):
        self.bookurl = set()

    def parse(self, response):
        for i in xrange(0, 89):
            url = 'http://book.douban.com/tag/编程?start=%s&type=S'% i*20
            yield Request(url=url, callback=self.item_parse)
        pass

    def item_parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = DoubanbookItem()
        # item['title'] = hxs.select('//*[@id="subject_list"]/ul/li[position()>0]/div[2]/h2/a/@title').extract()
        # item['link'] = hxs.select('//*[@id="subject_list"]/ul/li[position()>0]/div[2]/h2/a/@href').extract()
        # item['pub'] = hxs.select('//*[@id="subject_list"]/ul/li[position()>0]/div[2]/div[1]/text()').extract()
        # item['stars'] = hxs.select('//*[@id="subject_list"]/ul/li[position()>0]/div[2]/div[2]/span[1]/@class').extract()
        # item['rating_num'] = hxs.select('//*[@id="subject_list"]/ul/li[position()>0]/div[2]/div[2]/span[2]/text()').extract()
        # item['rating_people'] = hxs.select('//*[@id="subject_list"]/ul/li[position()>0]/div[2]/div[2]/span[3]/text()').extract()
        # item['desc'] = hxs.select('//*[@id="subject_list"]/ul/li[position()>0]/div[2]/p/text()').extract()


        sites = hxs.select('//*[@id="subject_list"]/ul/li[position()>0]/div[2]')

        for site in sites:
            if site.select('h2/a/@href').extract()[0] not in self.bookurl:
                item['title'] = site.select('h2/a/@title').extract()
                item['link'] = site.select('h2/a/@href').extract()
                self.bookurl.add(item['link'][0])
                item['pub'] = site.select('div[1]/text()').extract()
                # item['stars'] =re.search('\d+',''.join(site.select('/div[2]/span[1]/@class').extract())).group()
                item['stars'] = site.select('div[2]/span[1]/@class').re(r'stars:(\d+)')
                item['rating_num'] = site.select('div[2]/span[2]/text()').extract()
                item['rating_people'] = site.select('div[2]/span[3]/text()').extract()
                item['desc'] = site.select('p/text()').extract()
                yield item
