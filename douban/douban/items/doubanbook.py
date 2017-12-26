# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class DoubanbookItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    link = Field()
    pub = Field()
    stars = Field()
    rating_num = Field()
    rating_people = Field()
    desc = Field()
    pass

