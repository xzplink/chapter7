#!/usr/bin/evn python
# -*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2017/06/23

import sys
import cgi
import string
import random
import base64
from M2Crypto import RSA
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"
_random_len  = 16

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('0.0.0.0', port)

def random_generator():
    field = string.letters + string.digits
    return "".join(random.sample(field, _random_len))

class M2crpytoRSA(object):
    _key = sys.path[0] + "/private_key"

    def __init__(self, key_file=_key):
        self.privkey = RSA.load_key(key_file)

    def encrypt(self, text):
        try:
            cipher_text = self.privkey.private_encrypt(text, RSA.pkcs1_padding)
            return base64.b64encode(cipher_text)
        except:
            return ""

    def decrypt(self, text):
        try:
            plain_text = self.privkey.private_decrypt(base64.b64decode(text), RSA.pkcs1_padding)
            return plain_text
        except:
            return ""

class HandlerClass(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_error(400,"Get request is not support")

    def do_POST(self):
        ret_values = ""
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        print ctype
        print pdict
        print self.headers
        if ctype == 'text/plain':
            ret_values = random_generator()
        else:
            self.send_error(415, "only plain text data is supported.")
            return

        m2rsa = M2crpytoRSA()

        length = int(self.headers.getheader('content-length'))
        crypto_data = self.rfile.read(length)
        post_data = m2rsa.decrypt(crypto_data)
        post_data = eval(post_data)
        print post_data["uuid"]
        print post_data["rand"]
        print post_data["type"]
        print post_data["product"]

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        ret_values = m2rsa.encrypt(ret_values)
        self.wfile.write(ret_values)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()