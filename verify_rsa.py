#!/usr/bin/env python
# -*-encoding:UTF8-*-
# On 2017/06/07

import base64
import sys
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA

"""
runtime env: python-crypto > 2.2
"""

"""
# 伪随机数生成器
random_generator = Random.new().read
# rsa算法生成实例
rsa = RSA.generate(2048, random_generator)

# master的秘钥对的生成
private_pem = rsa.exportKey()

with open('master-private.pem', 'w') as f:
    f.write(private_pem)

public_pem = rsa.publickey().exportKey()
with open('master-public.pem', 'w') as f:
    f.write(public_pem)

# ghost的秘钥对的生成
private_pem = rsa.exportKey()
with open('ghost-private.pem', 'w') as f:
    f.write(private_pem)

public_pem = rsa.publickey().exportKey()
with open('ghost-public.pem', 'w') as f:
    f.write(public_pem)
"""

print "hello,word"

class PycryptoRSA(object):
    _random_generator = Random.new().read
    # print _random_generator
    _rsa = RSA.generate(2048, _random_generator)
    _crt = _rsa.publickey().exportKey()
    _key = _rsa.exportKey()
    # print "crt:",_crt
    # print "key:",_key

    def __init__(self,crt=_crt,key=_key):
        self.pubkey = crt
        self.secKey = key
        self.rsakey = RSA.importKey(self.secKey)

    def encrypt(self,text):
        cipher = Cipher_pkcs1_v1_5.new(self.rsakey)
        cipher_text = cipher.encrypt(text)
        # print cipher_text
        return base64.b64encode(cipher_text)

    def decrypt(self,text):
        cipher = Cipher_pkcs1_v1_5.new(self.rsakey)
        plain_text = cipher.decrypt(base64.b64decode(text), self._random_generator)
        print plain_text
        return plain_text

if __name__ == "__main__":
    test_str = """wo shi yi zhi xiao hua mao."""
    rsa = PycryptoRSA()
    cipher_text = rsa.encrypt(test_str)
    plain_text = rsa.decrypt(cipher_text)



