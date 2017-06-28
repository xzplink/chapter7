#!/usr/bin/env python

import BaseHTTPServer  
import SimpleHTTPServer  
import os  
import socket  
import ssl  
  
script_home = os.path.dirname(os.path.abspath(__file__))  
ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
port = 4443  
  
def main():  
    print ("simple https server, address:%s:%d, document root:%s" % (ip, port, script_home))  
  
    httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', port), SimpleHTTPServer.SimpleHTTPRequestHandler)  
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./ssl.pem', server_side=True)
    httpd.serve_forever()  
  
if __name__ == '__main__':  
    os.chdir(script_home)  
    main()  

