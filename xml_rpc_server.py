#!/usr/bin/env python

from SimpleXMLRPCServer import SimpleXMLRPCServer

class MyObject:
    def sayHello(self):
        return "hello xmlprc"


obj = MyObject()
server = SimpleXMLRPCServer(("localhost", 80))
server.register_instance(obj)

print "Listening on port 80"

server.serve_forever()
