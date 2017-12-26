#!/bin/bash
# -*- coding:utf-8 -*-
############################################
# File Name    : verify.sh
# Created By   : Suluo - sampson.suluo@gmail.com
# Creation Date: 2017-12-12
# Last Modified: 2017-12-12 01:56:04
# Descption    :
############################################

# set x

echo "$(date) Server start"
BASE_DIR=$(cd `dirname $0`;pwd)
cd ${BASE_DIR}
filename=verify.py
nohup python3 ${filename} -e xici>>./xici.log 2>&1 &
cd ..
scrapy crawl xici -s JOBDIR='./crawls/xici-1'
