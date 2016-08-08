# username: sampson
# -*- coding: utf-8 -*-
# time:2015
# funtions:

from scrapy import log

def warn(msg):
    log.msg(str(msg),level=log.WARNING)

def info(msg):
    log.msg(str(msg),level=log.INFO)

def debug(msg):
    log.msg(str(msg),level=log.DEBUG)