# -*- coding: UTF-8 -*- 
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from dazong.items import shopItem
from dazong.items import memberItem
from dazong.items import fansItem
from dazong.items import followsItem
from dazong.items import reviewsItem
from dazong.items import wishlistsItem
from dazong.items import checkinItem

class dazongSpider(BaseSpider):
    name = "pachong"
    allow_domains = ["http://www.dianping.com/"]

    '''start_urls = ["http://www.dianping.com/member/671109/reviews"]'''

    start_urls = ["http://www.dianping.com/member/6911699","http://www.dianping.com/member/2151360","http://www.dianping.com/member/35637735","http://www.dianping.com/member/3206768","http://www.dianping.com/member/22008100","http://www.dianping.com/member/3547753"]

    def parse(self, response):
        if '/reviews' in response.url:
            return self.reviews_parse(response)
        elif '/wishlists' in response.url:
            return self.wishlists_parse(response)
        elif '/checkin' in response.url:
            return self.checkin_parse(response)
        elif '/follows' in response.url:
            return self.follows_parse(response)
        elif '/fans' in response.url:
            return self.fans_parse(response)
        else:
            return self.member_parse(response)
      
    def member_parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = memberItem()
        item['consumer_name'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h2[@class="name"]/text()').extract()
        item['record_data'] = hxs.select('//div[@class="user-time"]/p[3]/text()').extract()
        item['lastlogon'] = hxs.select('//div[@class="user-time"]/p[4]/text()').extract()
        item['empirical'] = hxs.select('//div[@class="user-time"]/p[2]/text()').extract()
        item['contribution'] = hxs.select('//div[@class="user-time"]/p[1]/span[@id="J_col_exp"]/text()').extract()
        item['location'] = hxs.select('//span[@class="user-groun"]/text()').extract()
        item['label'] = hxs.select('//span[@id="J_usertag"]/em/text()').extract()
        item['gender'] = hxs.select('//span[@class="user-groun"]/i/@class').extract()
        yield item

        furl_attention=hxs.select('//div[@class="atten-info"]/a[1]/@href').extract()
        furl_fans=hxs.select('//div[@class="atten-info"]/a[2]/@href').extract()
        furl_visit=hxs.select('//div[@class="pic-list"]/ul/li/a/@href').extract()
        furl_reviews=hxs.select('//div[@class="modebox mode-hd dot-comm"]/div[2]/div[2]/a/@href').extract()
        furl_wishlists=hxs.select('//div[@class="modebox mode-hd collect"]/div[2]/div[2]/a/@href').extract()
        furl_checkin=hxs.select('//div[@class="modebox mode-hd sign-arrive"]/div[2]/div[2]/a/@href').extract()
        furl=furl_attention + furl_fans + furl_reviews + furl_wishlists + furl_checkin + furl_visit
        for furlsub in furl:
            furlsub="http://www.dianping.com"+furlsub
            yield Request(furlsub,callback = self.parse)

    def fans_parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = fansItem()
        item['consumer_name'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h2[@class="name"]/text()').extract()
        item['fans_name'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h6/a/text()').extract()
        item['fans_http'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h6/a/@href').extract()
        yield item

        furl=hxs.select('//div[@class="txt"]/div[@class="tit"]/h6/a/@href').extract()
        for furlsub in furl:
            furlsub="http://www.dianping.com"+furlsub
            yield Request(furlsub,callback = self.parse)
            
    def follows_parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = followsItem()
        item['consumer_name'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h2[@class="name"]/text()').extract()
        item['follows_name'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h6/a/text()').extract()
        item['follows_http'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h6/a/@href').extract()
        yield item
        furl=hxs.select('//div[@class="txt"]/div[@class="tit"]/h6/a/@href').extract()
        for furlsub in furl:
            furlsub="http://www.dianping.com"+furlsub
            yield Request(furlsub,callback = self.parse)

    def reviews_parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = reviewsItem()
        item['consumer_name'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h2[@class="name"]/text()').extract()
        item['shop_name'] = hxs.select('//div[@class="txt J_rptlist"]/div[@class="tit"]/h6/a/text()').extract()
        item['shop_http'] = hxs.select('//div[@class="txt J_rptlist"]/div[@class="tit"]/h6/a/@href').extract()
        item['shop_location'] = hxs.select('//div[@class="txt-c"]/div[@class="mode-tc addres"]/p/text()').extract()

        '''item['shop_grade'] = hxs.select('//div[@class="mode-tc comm-rst"]/span[1]/@title').extract()
            item['shop_taste'] = hxs.select('//div[@class="mode-tc comm-rst"]/span[2]/text()').extract()
            item['shop_environment'] = hxs.select('//div[@class="mode-tc comm-rst"]/span[3]/text()').extract()
            item['shop_serve'] = hxs.select('//div[@class="mode-tc comm-rst"]/span[4]/text()').extract()

	    if '/div[@class="mode-tc comm-rst"]/span[5]' in response:
            	item['shop_price'] = hxs.select('//div[@class="mode-tc comm-rst"]/span[5]/text()').extract()
            else:
		item['shop_price'] = 0'''

        item['reviews_data'] = hxs.select('//div[@class="mode-tc info"]/span/text()').extract()

        shop_reviews_nest= hxs.select('//div[@class="mode-tc comm-entry"]')
        for review in shop_reviews_nest :
            item.setdefault('shop_reviews',[]).append(''.join(review.select('text()').extract()))
            #dic.setdefault(key,[]).append(value)

            #item['shop_reviews'] = hxs.select('//div[@class="mode-tc comm-entry"]/text()').extract()
            yield item
            furl=hxs.select('//div[@class="pages-num"]/a/@href').extract()
            furl_reviews_supplement=hxs.select('//div[@class="modebox p-tabs-box"]/div[@class="tabs"]/a/@href').extract()           
            for furlsub in furl:
                furlsub="http://www.dianping.com"+ furl_reviews_supplement[0] + furlsub
                yield Request(furlsub,callback = self.parse)


    def checkin_parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = checkinItem()
        item['consumer_name'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h2[@class="name"]/text()').extract()
        item['checkin_time'] = hxs.select('//ul[@id="J_list"]/li/h6/span/text()').extract()
        item['checkin_shop'] = hxs.select('//ul[@id="J_list"]/li/h6/a/text()').extract()
        item['checkin_location'] = hxs.select('//ul[@id="J_list"]/li/p/text()').extract()
        #item['checkin_grade'] = hxs.select('//div[@class="sign-star"]/p[1]/span/@title').extract()
        #item['checkin_reviews'] = hxs.select('//div[@class="sign-star"]/p[1]/text()').extract()
        yield item
          
    def wishlists_parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = wishlistsItem()
        item['consumer_name'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h2[@class="name"]/text()').extract()
        item['wishlists_name'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h6/a/text()').extract()
        item['wishlists_http'] = hxs.select('//div[@class="txt"]/div[@class="tit"]/h6/a/@href').extract()
        item['wishlists_location'] = hxs.select('//div[@class="txt-c"]/div[@class="mode-tc addres"]/p/text()').extract()
        item['wishlists_data'] = hxs.select('//div[@class="mode-tc info"]/span[1]/i/text()').extract()
        yield item
        furl=hxs.select('//div[@class="pages-num"]/a/@href').extract()
        furl_wishlists_supplement=hxs.select('//div[@class="modebox p-tabs-box"]/div[@class="tabs"]/a/@href').extract()
        for furlsub in furl:
            furlsub="http://www.dianping.com"+ furl_wishlists_supplement[0] + furlsub
            yield Request(furlsub,callback = self.parse)
        '''def shop_parse(self, response):
            hxs = HtmlXPathSelector(response)
            item = shopItem()
	        item['good_name'] = hxs.select('//div[@class="shop-tit"]/div[@class="shop-name"]/h1[@itemprop="name itemreviewed"]/text()').extract()
	    item['good_price'] = hxs.select('//div[@class="rst-taste"]/span[1]/text()').extract()
	    item['good_estimate'] = hxs.select('//div[@class="rst-taste"]/span[2]/text()').extract()
	    item['good_address'] = hxs.select('//div[@class="shop-location"][1]/ul/li[1]/span[@itemprop="street-address"]/text()').extract()
	    item['areas_name'] = hxs.select('//div[@class="shop-location"][1]/ul/li[1]/a[@class="link-dk"]/span[@itemprop="locality region"]/text()').extract()
	    item['classification_name'] = hxs.select('//div[@class="breadcrumb"]/b[5]/a/span/text()').extract()
	    item['classes'] = hxs.select('//div[@class="header"]/ul/li[2]/a/strong/text()').extract()
            yield item
            furl_member=hxs.select('//div[@class="pic"]/a/@href').extract() 
            furl_shop=hxs.select('//div[@class="news-list"]/ul/li/h4/a/@href').extract()
            furl=furl_member + furl_shop
            for furlsub in furl:
                furlsub="http://www.dianping.com"+furlsub
	        yield Request(furlsub,callback = self.parse)'''
	




