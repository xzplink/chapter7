#!/usr/bin/evn python
# -*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2017/06/26

from M2Crypto import RSA


msg = 'well done, good luck to vector-zhang!'


print '*********************************************************'
print '公钥加密，私钥解密'
rsa_pub = RSA.load_pub_key("public_key")
ctxt = rsa_pub.public_encrypt(msg, RSA.pkcs1_oaep_padding)
ctxt64 = ctxt.encode('base64')
print ('密文:%s'% ctxt64)


rsa_pri = RSA.load_key("private_key")
txt = rsa_pri.private_decrypt(ctxt, RSA.pkcs1_oaep_padding)
print('明文:%s'% txt)



print '*************************************************************'
print '私钥加密，公钥解密'
ctxt_pri = rsa_pri.private_encrypt(msg, RSA.pkcs1_oaep_padding)
ctxt64_pri = ctxt_pri.encode('base64')
print ('密文:%s'% ctxt64_pri)

txt_pri = rsa_pub.public_decrypt(ctxt_pri, RSA.pkcs1_oaep_padding)
print('明文:%s'% txt_pri)



