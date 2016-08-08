#!/usr/bin/env python
# -*- coding:utf-8 -*-
#############################################
# Description: 
# File Name: items.py
# Author:Suluo-Sampson.suluo@gmail.com
# Last modified: 2016-05-26 18:55:12
# Python Release:2.7
###############################################

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class reviewsItem(Item):
    userID = Field()        #
    moviename = Field()
    movieID = Field()      #
    rating = Field()
    ratingdate = Field()
    comment = Field()
    pass

class moviesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    moviename = Field()
    movieID = Field()

    year = Field()
    director = Field()
    # scriptwriter = Field()
    actors = Field()
    film_types = Field()
    producer_coutry = Field()
    language = Field()
    # show_date = Field()
    # runtime = Field()
    # othername = Field()

    rating_num = Field()
    rating_stars = Field()
    rating_people = Field()

    intro = Field()
    doubanmembers_tag = Field()
    # award = Field()
    pass

class attentionsItem(Item):
    userID = Field()
    attentionID = Field()
    attentionUrl = Field()
    pass

class notesItem(Item):
    userID = Field()
    noteID = Field()
    notename = Field()
    notetext = Field()
    pass
