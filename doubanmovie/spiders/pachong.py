# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Selector,FormRequest
from scrapy.http import Request
import urllib
import requests
import re
from doubanmovie.items import reviewsItem,moviesItem,attentionsItem,notesItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import time


class PachongSpider(Spider):
    name = "pachong"
    allowed_domains = ["douban.com"]
    start_urls = (
        'https://www.douban.com/people/unlucky_strike/',
        'https://www.douban.com/people/heraunty/',
        'https://www.douban.com/people/47974911/'
    )

    # headers = {
        # 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'accept-encoding':'gzip, deflate',
        # 'accept-language':'zh-CN,zh;q=0.8',
        # 'cache-control':'max-age=0',
        # 'content-length':'161',
        # 'content-type':'application/x-www-form-urlencoded',
        # 'origin':'http://accounts.douban.com',
        # 'referer':'https://www.douban.com/accounts/login?redir=https%3A//www.douban.com/people/60012975/',
        # 'upgrade-insecure-requests':'1',
        # 'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
    # }

    def __init__(self):
        self.duplicatesurl = {}
        dispatcher.connect(self.spider_opened,signals.spider_opened)
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_opened(self):
        self.duplicatesurl['users'] = set()
        self.duplicatesurl['movies'] = set()

    def spider_closed(self):
        del self.duplicatesurl['users']
        del self.duplicatesurl['movies']


    def start_requests(self):
        yield Request('http://www.douban.com/accounts/login/',
                        meta={'cookiejar':1},
                        callback=self.login)

    def login(self,response):
        # login = requests.post(response.url,
        #                       headers = self.headers,
        #                       data={
        #                              'source':'None',
        #                              'redir':'https://www.douban.com/people/60012975/',
        #                              'form_email':'605976809@163.com',
        #                              'form_password':'123456789',
        #
        #                              'remember':'on',
        #                              'login':u'登录'
        #                       })

        hxs = Selector(response)
        if hxs.xpath('//*[@name="captcha-id"]/@value').extract():
            captchaID = hxs.xpath('//*[@name="captcha-id"]/@value').extract()[0]
            captchAdd = hxs.xpath('//*[@id="captcha_image"]/@src').extract()[0]
            urllib.urlretrieve(captchAdd,'captcha.jpg')
            captch = raw_input('please input the captcha:')
            yield FormRequest.from_response(response,
                                            meta =response.meta,
                                            # headers = self.headers,
                                            formdata={'source':'None',
                                                      'redir':'https://www.douban.com/people/unlucky_strike/',
                                                      'form_email':'605976809@163.com',
                                                      'form_password':'123456789',
                                                      'captcha-solution':captch,
                                                      'captcha-id':captchaID,
                                                      'remember':'on',
                                                      'login':u'登录'},
                                            callback=self.parse)
        else:
            yield FormRequest.from_response(response,
                                            meta ={'cookiejar':response.meta['cookiejar']},
                                            # headers = self.headers,
                                            formdata={'source':'None',
                                                      'redir':'https://www.douban.com/people/unlucky_strike/',
                                                      'form_email':'605976809@163.com',
                                                      'form_password':'123456789',
                                                      'remember':'on',
                                                      'login':u'登录'},
                                            callback=self.parse)



    # def after_login(self,response):
    #
    #     urls = hxs.xpath('//*[@id="statuses"]/div[2]/div/div/div[1]/div[1]/a/@href').extract()
    #     for url in urls:
    #         yield Request(url=url,callback=self.parse)
    #     pass

    def parse(self, response):
        if response.url not in self.duplicatesurl['users']:
            self.duplicatesurl['users'].add(response.url)

            hxs = Selector(response)
            if hxs.xpath('//*[@id="friend"]/h2/span/a/@href').extract():
                attentionsUrl = hxs.xpath('//*[@id="friend"]/h2/span/a/@href').extract()[0]
                yield Request(url=attentionsUrl,meta={'cookiejar':response.meta['cookiejar']},callback=self.attentions_parse)
            if hxs.xpath('//*[@id="movie"]/h2/span/a[last()]/@href').extract():
                reviewsUrl = hxs.xpath('//*[@id="movie"]/h2/span/a[last()]/@href').extract()[0]
                yield Request(url=reviewsUrl,callback=self.reviews_parse)
            notesUrl = hxs.xpath('//*[@id="db-usr-profile"]/div[@class="info"]/ul/li[4]/a/@href').extract()[0]
            yield Request(url=notesUrl,callback=self.notelist_parse)

        pass

    def attentions_parse(self,response):
        # print response.body
        hxs = Selector(response)
        # print 3333333
        item = attentionsItem()
        sites = hxs.xpath('//*[@class="article"]/dl')

        # print sites
        for site in sites:
            item['userID'] = re.findall('people/(.+)/contact',response.url)

            item['attentionID'] = site.xpath('dt/a/@href').re('people/(.+)/$')

            item['attentionUrl'] = site.xpath('dt/a/@href').extract()
            yield item
            # print item
            yield Request(url=item['attentionUrl'][0],meta={'cookiejar':response.meta['cookiejar']},callback=self.parse)

    def reviews_parse(self,response):
        hxs = Selector(response)
        # print 11111111
        item = reviewsItem()

        sites = hxs.xpath('//*[@class="article"]/div[2]/div[@class="item"]/div[@class="info"]/ul')
        # sites = hxs.xpath('//*[@class="article"]/div[2]/div[@class="item"]/div[@class="info"]')

        for site in sites:
            item['userID'] = re.findall('people/(.+)/collect',response.url)
            # print response.url
            item['moviename'] = site.xpath('li[@class="title"]/a/em/text()').extract()
            item['movieID'] = site.xpath('li[@class="title"]/a/@href').re('subject/(.+)/$')

            moviesUrl =site.xpath('li[@class="title"]/a/@href').extract()[0]
            yield Request(url=moviesUrl,callback=self.movie_parse)

            item['ratingdate'] = site.xpath('li[3]/span[@class="date"]/text()').extract()
            if re.findall('rating\d+-t',site.xpath('li[3]/span[1]/@class').extract()[0]):
                item['rating'] = site.xpath('li[3]/span[1]/@class').re('\d+')
            else:
                item['rating'] = [u'']
            if site.xpath('li[4]/span[@class="comment"]/text()').extract():
                item['comment'] = site.xpath('li[4]/span[@class="comment"]/text()').extract()
            else:
                item['comment'] = [u'']
            yield item
            # print item

        if hxs.xpath('//*[@class="paginator"]/span[@class="next"]/a/@href').extract():
            nextreviewsUrl = hxs.xpath('//*[@class="paginator"]/span[@class="next"]/a/@href').extract()[0]
            # print nextreviewsUrl
            yield Request(url=nextreviewsUrl,callback=self.reviews_parse)
        pass


    def movie_parse(self,response):
        if response.url not in self.duplicatesurl['movies']:
            self.duplicatesurl['movies'].add(response.url)
            hxs = Selector(response)

            item = moviesItem()

            item['moviename'] = hxs.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
            item['movieID'] = re.findall('subject/(.+)/$',response.url)
            item['year'] = hxs.xpath('//*[@id="content"]/h1/span[2]/text()').re('\d+')
            # print item['year']
            # item['director'] = hxs.select('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
            item.setdefault('director',[]).append('/'.join(hxs.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()))
            # item.setdefault('scriptwriter',[]).append('/'.join(hxs.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract()))
            # item.setdefault('actors',[]).append('/'.join(hxs.xpath('//*[@id="info"]/span[3]/span[2]/a[position()>0]/text()').extract()))
            item.setdefault('actors',[]).append('/'.join(hxs.xpath('//*[@rel="v:starring"]/text()').extract()))
            item.setdefault('film_types',[]).append('/'.join(hxs.xpath('//*[@property="v:genre"]/text()').extract()))

            linetemp = hxs.xpath('//*[@id="info"]/text()').extract()
            linetemp = [linetemp[i] for i in xrange(len(linetemp)) if re.findall('[^/\s]+',linetemp[i])]
            # print linetemp
            item['producer_coutry'] = linetemp[0]
            # print item['producer_coutry']
            item['language'] = linetemp[1]
            # print item['language']
            # item['show_time'] = hxs.select('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()').extract()
            # item.setdefault('show_date',[]).append('/'.join(hxs.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()').extract()))
            # item['runtime'] = hxs.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()').extract()
            # item['rating_num'] = hxs.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').re(r'(\d\.\d)')
            item.setdefault('rating_num',[]).append(''.join(hxs.xpath('//*[@typeof="v:Rating"]/strong/text()').re('\d\.\d')))
            # item['rating_stars'] = hxs.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[1]/@class').re(r'(\d+)')
            item['rating_stars'] = hxs.xpath('//*[@typeof="v:Rating"]/div/div[1]/@class').re('\d+')
            # item['rating_people'] = hxs.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()').re(r'(\d+)')
            item.setdefault('rating_people',[]).append(''.join(hxs.xpath('//*[@class="rating_people"]/span/text()').re('\d+')))

            item.setdefault('intro',[]).append(' '.join(hxs.xpath('//*[@id="link-report"]/span[1]/text()').re('\S+')))
            item.setdefault('doubanmembers_tag',[]).append(' '.join(hxs.xpath('//*[@class="tags-body"]/a/text()').extract()))
            # item.setdefault('award',[]).append('/'.join(hxs.xpath('//*[@id="content"]/div[2]/div[1]/div[5]/ul[position()>0]/li[position()>0]/text()').extract()))
            yield item
        pass

    def notelist_parse(self,response):
        hxs = Selector(response)
        # print 111111
        sites = hxs.xpath('//*[@class="note-header-container"]/h3')
        for site in sites:
            try:
                notesUrl = site.xpath('div/a[1]/@href').extract()[0]
                # print notesUrl
                yield Request(url=notesUrl,callback=self.note_parse)
            except IndexError,msg:
                pass

        if hxs.xpath('//*[@class="paginator"]/span[@class="next"]/a/@href').extract():
            nextnotesUrl = hxs.xpath('//*[@class="paginator"]/span[@class="next"]/a/@href').extract()[0]
            # print nextnotesUrl
            yield Request(url=nextnotesUrl,callback=self.notelist_parse)
        pass

    def note_parse(self,response):
        hxs = Selector(response)
        item = notesItem()

        item['noteID'] = re.findall('note/(.+)/$',response.url)
        item['notename'] = hxs.xpath('//*[@class="note-header note-header-container"]/h1/text()').extract()
        item['userID'] = hxs.xpath('//*[@class="note-header note-header-container"]/div/a[1]/@href').re('people/(.+)/$')
        item.setdefault('notetext',[]).append('\n'.join(hxs.xpath('//*[@id="link-report"]/text()').extract()))
        yield item
        # print item
        pass
