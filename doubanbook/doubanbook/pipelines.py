# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine,Table,MetaData

class DoubanbookPipeline(object):

    def process_item(self, item, spider):
        #创建到数据库的连接，echo=ture表示用logging输出调试结果
        mysql_engine = create_engine("mysql://root:123456@localhost:3306/test?charset=utf8&use_unicode=0",echo=True)
        #跟踪表属性
        metadata = MetaData(mysql_engine)
        user_table = Table('DoubanbookItem',metadata,autoload=True,autoload_with=mysql_engine)
        stmt = user_table.insert()
        stmt.execute(name=item['title'],url=item['link'],pub=item['pub'],stars=item['stars'],rating_num=item['rating_num'],
                     rating_people=item['rating_people'],desc=item['desc'])

        return item
