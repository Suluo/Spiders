# -*- coding: utf-8 -*-

from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
# from scrapy.spiders import CrawlSpider,Rule
# from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import re

from Tencentzhaopin.items import basicItem,detailItem


class PachongSpider(Spider):
    name = "pachong"
    allowed_domains = ["tencent.com"]
    start_urls = [
        'http://hr.tencent.com/position.php?&start=0#a'
    ]
    # rules = [
    #     Rule(LinkExtractor(allow=('/position.php\?&start=\d{,4}')),follow=True,callback='parse')
    # ]

    def parse(self, response):
        hxs = Selector(response)
        # print 1111111111
        item = basicItem()
        # sites = hxs.xpath('//*[@id="position"]/div[1]/table/tbody/tr[@class="even" or @class="odd"]')
        sites = hxs.xpath('//*[@id="position"]/div[1]/table/tr[@class="even"]|//*[@id="position"]/div[1]/table/tr[@class="odd"]')
        # print sites
        for site in sites:
            item['JobTitle'] = site.xpath('td[1]/a/text()').extract()
            item['DetailLink'] = 'http://hr.tencent.com/'+site.xpath('td[1]/a/@href').extract()[0]
            # detailurl = 'http://hr.tencent.com/'+item['DetailLink'][0]
            yield Request(url=item['DetailLink'],callback=self.detail_parse)
            item['JobType'] = site.xpath('td[2]/text()').extract()
            item['peoplenum'] = site.xpath('td[3]/text()').extract()
            item['location'] = site.xpath('td[4]/text()').extract()
            item['PostDate'] = site.xpath('td[5]/text()').extract()
            yield item
            # print item

        nexturl =  'http://hr.tencent.com/'+hxs.xpath('//*[@id="next"]/@href').extract()[0]
        # print nexturl
        yield Request(url=nexturl,callback=self.parse)
        pass

    def detail_parse(self,response):
        hxs = Selector(response)
        # print 11111
        item = detailItem()
        sites = hxs.xpath('//*[@id="position_detail"]/div/table')
        # print sites
        for site in sites:
            item['JobTitle'] = hxs.xpath('//*[@id="sharetitle"]/text()').extract()
            item['location'] = site.xpath('tr[2]/td[1]/text()').extract()
            item['JobType'] = site.xpath('tr[2]/td[2]/text()').extract()
            item['peoplenum'] = site.xpath('tr[2]/td[3]/text()').re('\d+')
            item.setdefault('responsibilities',[]).append(''.join(site.xpath('tr[3]/td/ul/li[position()>0]/text()').extract()))
            item.setdefault('requirements',[]).append(''.join(site.xpath('tr[4]/td/ul/li[position()>0]/text()').extract()))
            yield item
            # print item['JobTitle']

        pass
