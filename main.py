#!/usr/bin/env python
# -*- coding:utf-8 -*-
#############################################
# Description: 
# File Name: main.py
# Author:Suluo-Sampson.suluo@gmail.com
# Last modified: 2016-05-25 23:23:51
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

from scrapy import cmdline

cmdline.execute('scrapy crawl pachong'.split())
