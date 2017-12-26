# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Selector, FormRequest
from scrapy.http import Request
from ipagency.items import IP66Item
from pydispatch import dispatcher
from scrapy import signals


class Ip66Spider(Spider):
    name = 'ip66'
    allowed_domains = ["www.66ip.cn"]
    start_urls = [
        'http://www.66ip.cn'
    ]

    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self):
        self.duplicates['url'] = set()

    def spider_closed(self):
        del self.duplicates['url']

    def parse(self, response):
        hxs = Selector(response)
        content_urls = hxs.xpath('//ul[@class="textlarge22"]/li[position()>1]/a')
        for site in content_urls:
            url = site.xpath('@href').extract_first()
            province = site.xpath('text()').extract_first()
            content_url = "http://www.66ip.cn" + url
            yield Request(content_url, meta={'province': province})

    def parse_content(self, response):
        if response.url not in self.duplicates['url']:
            self.duplicates['url'].add(response.url)
            hxs = Selector(response)
            item = IP66Item()
            ip_list = hxs.xpath('//*[@class="main"]/div/div[1]/table/tr[position()>1]')
            for site in ip_list:
                item = {
                    "ip_port": site.xpath('td[1]/text()').extract_first() + ":" + site.xpath('td[2]/text()').extract_first(),
                    "address": site.xpath('td[3]/text()').extract_first(default="not found"),
                    "anonymity": site.xpath('td[4]/text()').extract_first(),
                    "proof": site.xpath('td[10]/text()').extract_first(),
                    "province": response.meta['province']
                }
                print (46, item)
                yield item
        # next_url = hxs.xpath('//*[@id="PageList"]/a[@class="pageCurrent"]/following-sibline::*[1]/@href').extract_first(default="not")
        next_url = hxs.xpath('//*[@id="PageList"]/a[-1]/@href').extract_first(default="not")
        if next_url != "not":
            url = "http://www.66ip.cn" + next_url
            yield Request(url=url, callback=self.parse)
