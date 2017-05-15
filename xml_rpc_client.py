#!/usr/bin/env python

import xmlrpclib

server = xmlrpclib.ServerProxy("http://localhost:80")

words = server.sayHello()

print "result:" + words