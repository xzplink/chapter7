import urllib2
body = urllib2.urlopen("http://www.baidu.com")
print body.read()