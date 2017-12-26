# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Selector, FormRequest
from scrapy.http import Request
from ipagency.items import GoubanjiaItem
from pydispatch import dispatcher
from scrapy import signals


class GoubanjiaSpider(Spider):
    name = 'goubanjia'
    allowed_domains = ["www.goubanjia.com"]
    start_urls = [
        'http://www.goubanjia.com/free/index.shtml'
    ]

    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened,signals.spider_opened)
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_opened(self):
        self.duplicates['url'] = set()

    def spider_closed(self):
        del self.duplicates['url']

    def parse(self, response):
        if response.url not in self.duplicates['url']:
            self.duplicates['url'].add(response.url)
            hxs = Selector(response)
            item = GoubanjiaItem()
            ip_list = hxs.xpath('//*[@id="list"]/table/tbody/tr')
            for site in ip_list:
                item = {
                    "ip_port": "".join(site.xpath('td[1]//text()').extract()),
                    "anonymity": site.xpath('td[2]/a/text()').extract_first(),
                    "http": site.xpath('td[3]/a/text()').extract_first(),
                    "address": site.xpath('td[4]/a/text()').extract(),
                    "operator": site.xpath('td[5]/text()').extract_first(default="not Found"),
                    "speed": site.xpath('td[6]/text()').extract_first(default="not found"),
                    "proof": site.xpath('td[7]/text()').extract_first(default="not found"),
                    "lifetime": site.xpath('td[8]/text()').extract_first()
                }
                yield item
        # next_url = hxs.xpath('//div[@class="wp-pagenavi"]/span[2]/following-sibling::*[1]/@href').extract_first(default="not")
        next_urls = hxs.xpath('//div[@class="wp-pagenavi"]/a/@href').extract()
        for next_url in next_urls:
            print ('goubanjiaitem', next_url)
            url = "http://www.goubanjia.com/free/" + next_url
            yield Request(url=url, callback=self.parse)
