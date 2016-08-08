# -*- coding: utf-8 -*-
import sys
import MySQLdb
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DropItem
import string
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer,    String, Unicode, DateTime

reload(sys)
sys.setdefaultencoding('utf8')

class DazongPipeline(object):

	def __init__(self):
		self.duplicates = {}
		dispatcher.connect(self.spider_opened, signals.spider_opened)
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_opened(self, spider):
		self.duplicates['memberItem'] = set()
		self.duplicates['fansItem'] = set()
		self.duplicates['followsItem'] = set()
		self.duplicates['reviewsItem'] = set()
		self.duplicates['reviewsItem1'] = set()
		self.duplicates['checkinItem'] = set()
		self.duplicates['checkinItem1'] = set()
		self.duplicates['wishlistsItem'] = set()
		self.duplicates['wishlistsItem1'] = set()

	def spider_closed(self, spider):
		del self.duplicates['memberItem']
		del self.duplicates['fansItem']
		del self.duplicates['followsItem']
		del self.duplicates['reviewsItem']
		del self.duplicates['reviewsItem1']
		del self.duplicates['checkinItem']
		del self.duplicates['checkinItem1']
		del self.duplicates['wishlistsItem']
		del self.duplicates['wishlistsItem1']

	def process_item(self, item, spider):

		mysql_engine = create_engine("mysql://root:1234@localhost:3306/dazongdianping?charset=utf8&use_unicode=0",echo=True)
		#创建到数据库的连接,echo=True 表示用logging输出调试结果
        metadata = MetaData(mysql_engine) #跟踪表属性
		if item.has_key('record_data'):  # 1
			if item['consumer_name'][0] in self.duplicates['memberItem']:
				raise DropItem("Duplicate item found: %s" % item)
			else:
				self.duplicates['memberItem'].add(item['consumer_name'][0])

			user_table = Table('memberItem', metadata, autoload=True, autoload_with=mysql_engine)
			stmt = user_table.insert()
			#item['label']= ' '.join(item['label'])
			genderjoin= ''.join(item['gender'])
			labeljoin= ''.join(item['label'])
			stmt.execute(consumer_name=item['consumer_name'][0], record_data=item['record_data'][0],lastlogon=item['lastlogon'][0],empirical=item['empirical'][0],contribution=item['contribution'][0],location=item['location'][0],label=labeljoin,gender=genderjoin)

		elif item.has_key('fans_name'): # 2

			if item['consumer_name'][0] in self.duplicates['fansItem']:
				raise DropItem("Duplicate item found: %s" % item)
			else:
				self.duplicates['fansItem'].add(item['consumer_name'][0])

			user_table = Table('fansItem', metadata, autoload=True, autoload_with=mysql_engine)
			stmt = user_table.insert()
			for i in range(len(item['fans_name'])):
				stmt.execute(consumer_name=item['consumer_name'][0], fans_name=item['fans_name'][i],fans_http=item['fans_http'][i])

		elif item.has_key('follows_name'): # 3

			if item['consumer_name'][0] in self.duplicates['followsItem']:
				raise DropItem("Duplicate item found: %s" % item)
			else:
				self.duplicates['followsItem'].add(item['consumer_name'][0])

			user_table = Table('followsItem', metadata, autoload=True, autoload_with=mysql_engine)
			stmt = user_table.insert()
			for i in range(len(item['follows_name'])):
				stmt.execute(consumer_name=item['consumer_name'][0], follows_name=item['follows_name'][i],follows_http=item['follows_http'][i])

		elif item.has_key('shop_name'): # 4

			if item['shop_name'][0] in self.duplicates['reviewsItem'] and item['consumer_name'][0] in self.duplicates['reviewsItem1'] :
				raise DropItem("Duplicate item found: %s" % item)
			else:
				self.duplicates['reviewsItem'].add(item['shop_name'][0])
				self.duplicates['reviewsItem1'].add(item['consumer_name'][0])
			
			user_table = Table('reviewsItem', metadata, autoload=True, autoload_with=mysql_engine)
			stmt = user_table.insert()
			for i in range(len(item['shop_name'])):
				stmt.execute(consumer_name=item['consumer_name'][0], shop_name=item['shop_name'][i],shop_http=item['shop_http'][i],shop_location=item['shop_location'][i],reviews_data=item['reviews_data'][i],shop_reviews=item['shop_reviews'][i])

		elif item.has_key('checkin_shop'): # 5

			if  item['consumer_name'][0] in self.duplicates['checkinItem1'] and item['checkin_time'][0] in self.duplicates['checkinItem']:
				raise DropItem("Duplicate item found: %s" % item)
			else:
				self.duplicates['checkinItem'].add(item['checkin_time'][0])
				self.duplicates['checkinItem1'].add(item['consumer_name'][0])

			user_table = Table('checkinItem', metadata, autoload=True, autoload_with=mysql_engine)
			stmt = user_table.insert()
			for i in range(len(item['checkin_shop'])):
				stmt.execute(consumer_name=item['consumer_name'][0], checkin_time=item['checkin_time'][i],checkin_shop=item['checkin_shop'][i],checkin_location=item['checkin_location'][i])

		else:      #item.has_key(' wishlists_name')  6

			if  item['consumer_name'][0] in self.duplicates['wishlistsItem1'] and item['wishlists_name'][0] in self.duplicates['wishlistsItem']:
				raise DropItem("Duplicate item found: %s" % item)
			else:
				self.duplicates['wishlistsItem'].add(item['wishlists_name'][0])
				self.duplicates['wishlistsItem1'].add(item['consumer_name'][0])

			user_table = Table('wishlistsItem', metadata, autoload=True, autoload_with=mysql_engine)
			stmt = user_table.insert()
			for i in range(len(item['wishlists_name'])):
				stmt.execute(consumer_name=item['consumer_name'][0], wishlists_name=item['wishlists_name'][i],wishlists_http=item['wishlists_http'][i],wishlists_location=item['wishlists_location'][i],wishlists_data=item['wishlists_data'][i])

		return item

'''consumer_names = ''.join(item['consumer_name'])
	   	consumer_names = consumer_names.strip() 
		empiricals = ''.join(item['empirical'])
	   	empiricals = empiricals.strip()

 metadata.create_all(mysql_engine)  #在数据库中生成表
        class User(object): pass #创建一个映射类
        mapper(User, user_table) #把表映射到类
        Session = sessionmaker() #创建了一个自定义了的 Session类
        Session.configure(bind=mysql_engine)#将创建的数据库连接关联到这个session
        session = Session()
        u = User()
        #u.consumer_no=1
        u.consumer_name=item['consumer_name'][0]
        u.record_data=item['record_data'][0]
        u.lastlogon=item['lastlogon'][0]
        u.empirical=item['empirical'][0]
        session.add(u)#在session中添加内容
        session.flush() #保存数据
        session.commit() #数据库事务的提交,sisson自动过期而不需要关闭'''
