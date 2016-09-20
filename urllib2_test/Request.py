#!/usr/bin/env python
#-*-encoding:UTF8-*-
import urllib2
body = urllib2.urlopen("http://www.baidu.com")
print body.read()