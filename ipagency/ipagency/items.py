# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field
import scrapy


class IpagencyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class XiciItem(Item):
    country = Field()
    ip_port = Field()
    address = Field()
    anonymity = Field()
    http = Field()
    speed = Field()
    connect_time = Field()
    lifetime = Field()
    proof = Field()


class GoubanjiaItem(Item):
    ip_port = Field()
    anonymity = Field()
    http = Field()
    address = Field()
    operator = Field()
    speed = Field()
    proof = Field()
    lifetime = Field()


class IP66Item(Item):
    ip_port = Field()
    address = Field()
    anonymity = Field()
    proof = Field()


class MimvpItem(Item):
    country = Field()
    ip_port = Field()
    address = Field()
    http = Field()
    speed = Field()
    connect_time = Field()
    lifetime = Field()
    proof = Field()
