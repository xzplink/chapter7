#!/usr/bin/evn python
# -*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2017/06/26

import sys
import os
import logging
import urllib
import urllib2
import socket
import base64
from M2Crypto import RSA

socket.setdefaulttimeout(5)
RET_FLAG        = 0 # 0 auth failed, 1 auth success
UUID_FILE_PATH  = "/var/waf/waf_uuid"
RAND_FILE_PATH  = "/var/waf/waf_rand"
AUTH_FILE_PATH  = "/var/waf/waf_auth"
TYPE_UNKNOWN    = 0
TYPE_WAF        = 1
TYPE_NVS        = 2
TYPE_NGFW       = 3
AUTH_UNKNOWN    = 0
AUTH_STAND      = 1
AUTH_ON_LINE    = 2


def get_dev_uuid():
    if not os.path.exists(UUID_FILE_PATH):
        os.popen("/usr/bin/uuidgen > %s" % UUID_FILE_PATH)
    output = os.popen("cat %s|tr -d '\n'" % UUID_FILE_PATH).read()
    if output:
        return output
    else:
        return ""

def get_dev_rand():
    if os.path.exists(RAND_FILE_PATH):
        output = os.popen("cat %s|tr -d '\n'" % RAND_FILE_PATH).read()
        if output:
            return output
    else:
        return "4PCRlvnihYZkP6"

def get_auth_type():
    if os.path.exists(AUTH_FILE_PATH):
        output = os.popen("cat %s" % AUTH_FILE_PATH).read()
        if output == "1":
            return AUTH_STAND
        elif output == "2":
            return AUTH_ON_LINE
        else:
            return AUTH_UNKNOWN
    else:
        return AUTH_UNKNOWN

def get_product_type():
    output = os.popen("/bin/hostname").read()
    if output:
        if output.find("waf") != -1:
            return TYPE_WAF
        elif output.find("nvs") != -1:
            return TYPE_NVS
        elif output.find("ngfw") != -1:
            return TYPE_NGFW
        else:
            return TYPE_UNKNOWN
    else:
        return TYPE_UNKNOWN

class M2crpytoRSA(object):
    _crt = sys.path[0] + "/public_key"

    def __init__(self, crt_file=_crt):
        self.pubkey = RSA.load_pub_key(crt_file)

    def encrypt(self, text):
        try:
            cipher_text = self.pubkey.public_encrypt(text, RSA.pkcs1_padding)
            return base64.b64encode(cipher_text)
        except:
            return ""

    def decrypt(self, text):
        try:
            plain_text = self.pubkey.public_decrypt(base64.b64decode(text), RSA.pkcs1_padding)
            return plain_text
        except:
            return ""

class AuthRequest(object):
    _post_data = {}

    def __init__(self, url):
        self.url = url
        self.uuid = get_dev_uuid()
        self.rand = get_dev_rand()
        self.type = get_auth_type()
        self.product = get_product_type()
        self.m2rsa = M2crpytoRSA()

    def _prepare(self):
        self._post_data["uuid"] = self.uuid
        self._post_data["rand"] = self.rand
        self._post_data["type"] = self.type
        self._post_data["product"] = self.product
        # print self._post_data

    def request(self):
        self._prepare()
        headers = {'Content-type':'text/plain'}
        post_data = self.m2rsa.encrypt(str(self._post_data))

        req = urllib2.Request(url = self.url, headers = headers, data = post_data)
        response = urllib2.urlopen(req)
        if response:
            return response.read()
        else:
            return ""

    def parse_response(self, res):
        global RET_FLAG
        if res:
            new_rand = self.m2rsa.decrypt(res)
            if new_rand: # update new rand to the random file
                print new_rand
                os.popen("echo %s > %s" % (new_rand, RAND_FILE_PATH))
                RET_FLAG = 1 # means auth success

    def run(self):
        res = self.request()
        self.parse_response(res)

def usage():
    print "Usage: %s http://xxx" % sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    else:
        req_url = sys.argv[1]
        handler = AuthRequest(req_url)
        handler.run()
        if RET_FLAG:
            print 1
        else:
            print 0
