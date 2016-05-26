#!/usr/bin/env python
# -*- coding:utf-8 -*-
#############################################
# Description: 
# File Name: pipelines.py
# Author:Suluo-Sampson.suluo@gmail.com
# Last modified: 2016-05-26 18:55:42
# Python Release:2.7
###############################################

import logging
import logging.handlers
import logging.config
import traceback
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine,MetaData,Table
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class DoubanmoviePipeline(object):

    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened,signals.spider_opened)
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_opened(self):
        self.duplicates['reviewsItem'] = set()
        self.duplicates['moviesItem'] = set()
        self.duplicates['attentionsItem'] = set()
        self.duplicates['notesItem'] = set()
        pass

    def spider_closed(self):
        del self.duplicates['reviewsItem']
        del self.duplicates['moviesItem']
        del self.duplicates['attentionsItem']
        del self.duplicates['notesItem']
        pass

    def process_item(self, item, spider):
        mysql_engine = create_engine("mysql://root:123456@localhost:3306/Doubanmovie?charset=utf8&use_unicode=0",echo=True)
        metadata = MetaData(mysql_engine)
        if 'ratingdate' in item.keys():
            if item['userID'][0]+item['movieID'][0] not in self.duplicates['reviewsItem']:
                self.duplicates['reviewsItem'].add(item['userID'][0]+item['movieID'][0])

                user_table = Table('reviewsItem',metadata,autoload=True,autoload_with=mysql_engine)
                stmt = user_table.insert()
                stmt.execute(userID=item['userID'],movieID=item['movieID'],moviename=item['moviename'],
                            rating=item['rating'],ratingdate=item['ratingdate'],comment=item['comment'])

        elif 'director' in item.keys():
            if item['movieID'][0] not in self.duplicates['moviesItem']:
                self.duplicates['moviesItem'].add(item['movieID'][0])

                user_table = Table('moviesItem',metadata,autoload=True,autoload_with=mysql_engine)
                stmt = user_table.insert()
                stmt.execute(movieID=item['movieID'],moviename=item['moviename'],year=item['year'],
                            director=item['director'],actors=item['actors'],film_types=item['film_types'],
                            producer_coutry=item['producer_coutry'],language=item['language'],
                            rating_num=item['rating_num'],rating_stars=item['rating_stars'],rating_people=item['rating_people'],
                            intro=item['intro'],doubanmembers_tag=item['doubanmembers_tag'])

        elif 'attentionID' in item.keys():
            if item['userID'][0]+item['attentionID'][0] not in self.duplicates['attentionsItem']:
                self.duplicates['attentionsItem'].add(item['userID'][0]+item['attentionID'][0])

                user_table = Table('attentionsItem',metadata,autoload=True,autoload_with=mysql_engine)
                stmt = user_table.insert()
                stmt.execute(userID=item['userID'],attentionID=item['attentionID'],attentionUrl=item['attentionUrl'])

        elif 'noteID' in item.keys():
            if item['userID'][0]+item['noteID'][0] not in self.duplicates['notesItem']:
                self.duplicates['notesItem'].add(item['userID'][0]+item['noteID'][0])

                user_table = Table('notesItem',metadata,autoload=True,autoload_with=mysql_engine)
                stmt = user_table.insert()
                stmt.execute(userID=item['userID'],noteID=item['noteID'],notename=item['notename'],notetext=item['notetext'])

        return item
