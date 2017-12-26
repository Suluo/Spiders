# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Selector
from scrapy.http import Request
from ipagency.items import MimvpItem
from pydispatch import dispatcher
from scrapy import signals


class MimvpSpider(Spider):
    name = 'mimvp'
    allowed_domains = ["proxy.mimvp.com"]
    start_urls = [
        "https://proxy.mimvp.com/free.php?proxy=in_tp",
        "https://proxy.mimvp.com/free.php?proxy=in_hp",
        "https://proxy.mimvp.com/free.php?proxy=out_tp",
        "https://proxy.mimvp.com/free.php?proxy=out_hp",
        "https://proxy.mimvp.com/free.php?proxy=in_socks",
        "https://proxy.mimvp.com/free.php?proxy=out_socks",
    ]

    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self):
        self.duplicates['url'] = set()

    def spider_closed(self):
        del self.duplicates['url']

#    def make_requests_from_url(self, url):
#        return Request(url=url, meta={"download_timeout": 30}, callback=self.parse)

    def parse(self, response):
        if response.url not in self.duplicates['url']:
            self.duplicates['url'].add(response.url)
            hxs = Selector(response)
            item = MimvpItem()
            ip_list = hxs.xpath('//*[@id="ip_list"]/tr[position()>1]')
            for site in ip_list:
                item = {
                    "country": site.xpath('td[1]/img/@alt').extract_first(default='Cn'),
                    "ip_port": site.xpath('td[2]/text()').extract_first() + ":" + site.xpath('td[3]/text()').extract_first(),
                    "address": site.xpath('td[4]/a/text()').extract_first(default="not found"),
                    "anonymity": site.xpath('td[5]/text()').extract_first(),
                    "http": site.xpath('td[6]/text()').extract_first(),
                    "speed": site.xpath('td[7]/div/@title').extract_first(default="not found"),
                    "connect_time": site.xpath('td[8]/div/@title').extract_first(default="not found"),
                    "lifetime": site.xpath('td[9]/text()').extract_first(),
                    "proof": site.xpath('td[10]/text()').extract_first()
                }
                print (46, item)
                yield item
        next_url = hxs.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract_first(default="not found")
        if next_url != "not found":
            url = "http://www.xicidaili.com" + next_url
            yield Request(url=url, callback=self.parse)
