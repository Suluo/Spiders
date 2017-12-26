#!/usr/bin/env python
# -*- coding:utf-8 -*-
############################################
# File Name    : verify.py
# Created By   : Suluo - sampson.suluo@gmail.com
# Creation Date: 2017-12-12
# Last Modified: 2017-12-12 01:55:27
# Descption    :
# Version      : Python 2.7
############################################
from __future__ import division
from pymongo import MongoClient
import logging
import logging.handlers
# import traceback
# import os
import argparse
import requests
import telnetlib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# file
logging.basicConfig(
    format="[ %(levelname)1.1s  %(asctime)s  %(module)s:%(lineno)d  %(name)s  ]  %(message)s",
    datefmt="%y%m%d %H:%M:%S",
    filemodel="a",
    filename="./data_dump.log",
    stream=sys.stdout, # 默认stderr, 和filename同时指定时，stream被忽略
    level=logging.INFO
)

# console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger(__name__).addHandler(console)

# Now, define a couple of other loggers which might represent areas in your
# application:
logger = logging.getLogger(__file__)
client = MongoClient(host='127.0.0.1', port=27017).ip


class TestProxy(object):
    def __init__(self):
        self.url = 'http://www.baidu.com'
        self.timeout = 10

    def request_verify(self, ip, http='http'):
        proxies = {http: http + "://" + ip}
        try:
            requests.get(self.url, proxies=proxies)
        except:
            return False
        else:
            return True

    def telnet_verify(self, ip, port):
        try:
            telnetlib.Telnet('127.0.0.1', port='80', timeout=self.timeout)
        except:
            return False
        else:
            return True


def mongo_verify(spider_name="xici"):
    testproxy = TestProxy()
    for table in [spider_name]:
        if client[table].find().count() > 0:
            for ip in client[table].find({}, {"_id": 0}):
                if testproxy.request_verify(ip['ip'], ip['http']):
                    continue
                client[table].remove({'ip': ip['ip']})


def main(spider_name):
    mongo_verify(spider_name)
    return spider_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--spider_name', type=str, default="xici", help='spider_name-xici')
    args = parser.parse_args()
    main(args.spider_name)
