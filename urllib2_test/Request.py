#!/usr/bin/env python
#-*-encoding:UTF8-*-

import logging
import urllib2

try:
    socket = urllib2.urlopen("http://cn.bing.com/search?q=ip:/**/218.94.157.126&go=&qs=n&qs=n")
    content = socket.read(1024)
    print content
    # print len(content)
    socket.close()
except Exception,e:
    logging.error("urlopen error:" + str(e))

# """some website don't allow spider to scrapy web content"""
# headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
# try:
#     req = urllib2.Request(url="http://blog.csdn.net/deqingguo",headers=headers)
#     socket = urllib2.urlopen(req)
#     content = socket.read()
#     print content
#     socket.close()
# except Exception,e:
#     logging.error("urlopen error:" + str(e))