# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from pymongo import MongoClient
from datetime import datetime, timedelta
import re
import ipaddress


class IpagencyPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        self.client = MongoClient(host=settings['MONGO_HOST'],
                                  port=settings['MONGO_PORT']).ip

    def process_item(self, item, spider):
        postItem = dict(item)
        try:
            ip = postItem['ip_port'].strip().split(':')[0]
            ipaddress.IPv4Network(ip)
        except Exception:
            print('netmask is invalid for IPv4:', postItem.get('ip_port', None))
            return item

        print ('mongo', spider.name, item)
        postItem['discovery_time'] = datetime.utcnow()
        expire_time = postItem['discovery_time'] + \
            timedelta(seconds=self._get_time(postItem.get('lifetime', "1小时")))
        postItem['expire_time'] = expire_time

        db = self.client[spider.name]
        db.ensure_index("expire_time", expireAfterSeconds=0)

        if db.find({'ip_port': postItem['ip_port']}).count() > 0:
            db.update({"ip_port": postItem['ip_port']}, postItem)
            print ("Update", postItem)
        else:
            db.insert_one(postItem)
            print ("Insert", postItem)
        return item

    def _format_check(self, postItem):
        # 检验ip格式
        if "ip" not in postItem \
                or len(postItem['ip']) > 21:
            return False
        ip = postItem['ip'].split('.|:')
        if len(ip) != 5:
            return False
        for i in ip[:-1]:
            if int(i) > 255:
                return False
        return True

    def _get_time(self, timestr):
        time_map = {
            "天": 24*3600,
            "小时": 3600,
            "分钟": 60
        }
        for timend in time_map.keys():
            if timend in timestr:
                timeint = int(re.match("\d+", timestr).group(0))
                expire_time = timeint * time_map[timend]
                return expire_time
        else:
            return time_map['小时']*5
