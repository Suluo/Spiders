# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine,MetaData,Table
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class TencentzhaopinPipeline(object):

    def __init__(self):
        self.duplicates={}
        dispatcher.connect(self.spider_open,signals.spider_opened)
        dispatcher.connect(self.spider_close,signals.spider_closed)

    def spider_open(self):
        self.duplicates['basicItem'] = set()
        self.duplicates['detailItem'] = set()
        pass

    def spider_close(self):
        del self.duplicates['basicItem']
        del self.duplicates['detailItem']
        pass

    def process_item(self, item, spider):
        mysql_engine = create_engine("mysql://root:123456@localhost:3306/test?charset=utf8&use_unicode=0",echo=True)
        metadata = MetaData(mysql_engine)
        if 'DetailLink' in item.keys():
            if item['DetailLink'] not in self.duplicates['basicItem']:
                self.duplicates['basicItem'].add(item['DetailLink'])

                user_table = Table('tecentzhaopinbasicItem',metadata,autoload=True,autoload_with=mysql_engine)
                stmt = user_table.insert()
                stmt.execute(JobTitle=item['JobTitle'],DetailLink=item['DetailLink'],JobType=item['JobType'],
                             peoplenum=item['peoplenum'],location=item['location'],PostDate=item['PostDate'])
        else:
            user_table = Table('tecentzhaopindetailItem',metadata,autoload=True,autoload_with=mysql_engine)
            stmt = user_table.insert()
            stmt.execute(JobTitle=item['JobTitle'],location=item['location'],JobType=item['JobType'],
                         peoplenum=item['peoplenum'],responsibilities=item['responsibilities'],requirements=item['requirements'])
