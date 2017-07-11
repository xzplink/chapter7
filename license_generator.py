#!/usr/bin/env python
# -*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2017/06/07

# import rsa
import sys
import os
import datetime
import string
import random
import logging


# reload(sys)
# sys.setdefaultencoding('utf8')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s')

private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEqgIBAAKCAQEAnNH3JgYKV8yiRDalgPZojEXM1h9Ou9gIaQDk0b91NeieTu8K
r5UR2z09GOUrldOEpA1cdd1TZempESKcHqLYSfdLUJVVj2agOcdzBIk0beyB2S9S
JTWeEa0AKQ/N5zrTirmESBnV4h5kmERz0Q4aYhCEvUM/tpRrbfLDYSg/tVpWPIF8
vjmkSqrNRzoXzIRMA8excms06G7yX7lIWOy4+37/uFeyeeJxp7pWiHv5eGRWoG0f
rRn6wkAQtCEPG+TBypoxBDBFHuP/TgNjVmu3FmMaC09EWO6jeIJntfhQtqOCsaAm
Xb2wlApSTClhGKhdI5IZS+EmbyBkmICPTzp0hwIDAQABAoIBAGeLt/4SVPf+NVKH
JqbNjOC6IfNsPqeHkJ4MqgnYukL7MrR53/tpmZ3ChLoQb8QBIv7Tl653kl6jdy/K
Q31zFw9XyxINWK5UHA2qpUZkdgry9BX8yeepzJJtQcLbHaDFVfKuZirZbEFewhtM
b5ClGESSFaOGaOZcf1dPpKRRM73dE7MVug7PU4/j/nAY+GRdrPl5epcBukNtQaRQ
oK7c/ZQgDRUMXRp99GkU2Fbi4MuYxkrbo2uQKgtgMjxRW5vNcp0FmyiKdtO2UDAV
v1EcUbCqMEhuEpjfCB2/uzXiQOR3tbtt/UjEbyvRal3HruN0Z+EFKVp9WasDyzqV
9zB+JnkCgYkAqPEpBvnI6QYPpYLSzIWNgSf07kuJaOWarkv2w5mawmJi2EmvBXvi
b8rDzku6SzfcOkdzZKNp0nmOoU4zWBfHfq1V0EolYZ7wdNbbHPO87xSe8DfQbYsR
9OA6jkOBhgDUkneMi0ApmDwcpHtdIOhi7Qntwuy8xvmI0tWAZ/zJr1OALJRPSjsn
0wJ5AO2hsIhTeG0CO72Mqnl+nvMoQdhjRm17KudkzfeVD876pJh2d0t0zgMMjXJW
DGwvupywWELwNGIR2fJ/DDUTYzTyloqLKSBtBLaUGqHiLDtp1oyram/kHFXvApvs
OdLcRCMQnI7aAVxRYy6tg+PdS1Yuij2nkzzj/QKBiQCYlU8/zKQnymChVPn83HaE
e0kdXD3b7tv4pgVWfkonXGL4A/y+kDhgTZrxnLXCL86JGHVhJLJz9XPbvlxjKP72
K6mAuSbv93QnotI9YOp4aIBwZ4ipF1z9dPON/+xg0ikrrCvUrPukUk5wRDdFfH20
py4FynlpoIByI4CY6thhsKHoIX9HhQwfAnkAqFgPk8RuX+thHxtz+bY2LNSsMPvD
fPPwpRTIxUiYdm0iBdCHGrGY8JgH7KQBEPOPJEnZfTJmKcOzvxM6Nq+RbIUfGO8V
J5+T4zRw2ZY896o3EFivgqz7VfWIx6VGIZdhveWaw6i1pg0SUpMiCF9Ra7B0xtDc
ghqRAoGIFVA3mBdxBwyixZd2CsEVhV7228jWJFtjmKN1LZ0EIW7bhWzvm+KUn1Pe
B9iub3EGgN0PZDwvjrPBAgNtadh4IHdQBnut0xr7KvT2xq+cfuqRvJO2bWK48+Zn
147NMRMDpRZjLw/WovnyIwkUoSzoQlHq9z9p5S8E4ZC/pwnZcx+AkXZg6iwBZA==
-----END RSA PRIVATE KEY-----"""

public_key = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAnNH3JgYKV8yiRDalgPZojEXM1h9Ou9gIaQDk0b91NeieTu8Kr5UR
2z09GOUrldOEpA1cdd1TZempESKcHqLYSfdLUJVVj2agOcdzBIk0beyB2S9SJTWe
Ea0AKQ/N5zrTirmESBnV4h5kmERz0Q4aYhCEvUM/tpRrbfLDYSg/tVpWPIF8vjmk
SqrNRzoXzIRMA8excms06G7yX7lIWOy4+37/uFeyeeJxp7pWiHv5eGRWoG0frRn6
wkAQtCEPG+TBypoxBDBFHuP/TgNjVmu3FmMaC09EWO6jeIJntfhQtqOCsaAmXb2w
lApSTClhGKhdI5IZS+EmbyBkmICPTzp0hwIDAQAB
-----END RSA PUBLIC KEY-----"""

HDMODE = [[1210, 1220, 2820], [2810, 5830, 6830, 5930, 6930], [8900, 8930]]
HDWARE_CONF = {}
VERIFY_STR = ""
PLAIN_CODE = ""

# class PycryptoRSA(object):
#     def __init__(self, crt=public_key, key=private_key):
#         self.pubkey = rsa.PublicKey.load_pkcs1(crt)
#         self.privkey = rsa.PrivateKey.load_pkcs1(key)
#
#     def generate_keypair(self):
#         (crt, key) = rsa.newkeys(2048)
#         try:
#             fd =  open('public.pem','w+')
#             fd.write(crt.save_pkcs1())
#             fd.close()
#
#             fd = open('private.pem','w+')
#             fd.write(key.save_pkcs1())
#             fd.close()
#         except Exception,e:
#             logging.error("generate keypair faild:" + str(e))
#
#     def encrypt(self, text):
#         try:
#             cipher_text = rsa.encrypt(text, self.pubkey)
#             return cipher_text
#         except Exception,e:
#             logging.error( "fatal error encrypt():" + str(e))
#             return ""
#
#     def decrypt(self, text):
#         try:
#             plain_text = rsa.decrypt(text, self.privkey)
#             return plain_text
#         except Exception,e:
#             logging.error("fatal error decrypt():" + str(e))
#             return ""
#
#     def sign(self, text):
#         try:
#             signature = rsa.sign(text, self.privkey, 'SHA-256')
#             return signature
#         except Exception,e:
#             logging.error("fatal error sign():" + str(e))
#             return ""
#
#     def verify(self, text, signature):
#         try:
#            ret = rsa.verify(text, signature, self.pubkey)
#            print ret
#         except Exception,e:
#             logging.error("fatal error verify():" + str(e))
#             return ""

class LicenseManager(object):
    _random_len = 16
    _lic_name = "/waf.lic"

    def __init__(self,begin,end,serno,feature,code,type=0):
        # self.lic_rsa = PycryptoRSA()
        self.company = ""#"
        self.code = code
        self.lic_file = sys.path[0] + self._lic_name

    def random_generator(self):
        field = string.letters + string.digits
        return "".join(random.sample(field, self._random_len))

    def _verify_challenge_code(self):
        global HDWARE_CONF,PLAIN_CODE,VERIFY_STR
        from hardware_info import PycryptoAES
        lic_aes = PycryptoAES()

        try:
            PLAIN_CODE = lic_aes.decrypt(self.code)
            HDWARE_CONF = eval(PLAIN_CODE)
            logging.debug("HDWARE_CONF: %s" % HDWARE_CONF)

            if HDWARE_CONF and len(HDWARE_CONF) != 9:
                return 1

            # 1、verify hardware configure info
            target = int(HDWARE_CONF["modelno"].split('-')[1])

            if target in HDMODE[0]:
                if int(HDWARE_CONF["mem_total"]) > 4:
                    return 2
                if HDWARE_CONF['cpu_type'].find("i3") != -1:
                    return 3
            elif target in HDMODE[1]:
                if int(HDWARE_CONF["mem_total"]) > 8:
                    return 4
                if HDWARE_CONF['cpu_type'].find("i7") != -1:
                    return 5
            elif target in HDMODE[2]:
                if int(HDWARE_CONF["mem_total"]) > 8:
                    return 6
            else:
                return 7
            # 2、verify time, if abs(given_time - time_now) >= 2, return failed
            time_now = datetime.datetime.now().strftime("%Y/%m/%d")
            # print "time_now is: %s" % time_now

            # 3、generater verify code
            verify_dic = {}
            verify_dic["core_num"] = HDWARE_CONF["core_num"]
            verify_dic["mem_total"] = HDWARE_CONF["mem_total"]
            # verify_dic["hdisk_sernum"] = HDWARE_CONF["hdisk_sernum"]
            verify_dic["cpu_type"] = HDWARE_CONF["cpu_type"]
            verify_dic["cpu_id"] = HDWARE_CONF["cpu_id"]
            verify_dic["mb_uuid"] = HDWARE_CONF["mb_uuid"]
            verify_dic["mac_list"] = HDWARE_CONF["mac_list"]
            VERIFY_STR = str(verify_dic)

            return 0
        except Exception,e:
            logging.error("failed:" + str(e))
            return 8

    def _prepare(self):
        ret = self._verify_challenge_code()
        if ret != 0:
            logging.error("Verify challenge code failed, error code:%s" % ret)
            sys.exit(0)

        from hardware_info import get_text_md5
        if VERIFY_STR:
            self.hdmd5 = get_text_md5(VERIFY_STR)

        if HDWARE_CONF["user"]:
            self.company = HDWARE_CONF["user"]

        if HDWARE_CONF["modelno"]:
            self.model = HDWARE_CONF["modelno"]

        if HDWARE_CONF["modelno"] and self.serial_num:
            model = str(HDWARE_CONF["modelno"]).split(' ')[1]
            file_name = "%s[%s][%s][%s].lic" % (HDWARE_CONF["user"], model, self.serial_num, self.license_end)
            # print file_name
            # file_name = file_name.decode()
            self.lic_file = sys.path[0] + "/" + file_name
            # self.lic_file = self.lic_file.decode('utf8')
            logging.debug("lic_file is: %s" % self.lic_file)

    def encode_file(self):
        os.system("./wafrsa -e -i %s -o %s -p %s" % (self.lic_file, self.lic_file, "yourpassword"))

    def run(self):
        self._prepare()
        try:
            lic_str = self.company
            logging.debug("lic_str:%s \nlic_str len:%d" %(lic_str, len(lic_str)))
            # lic_str = lic_str.encode('utf8')
            # cryptor_text = self.lic_rsa.encrypt(lic_str)

            lic = open(self.lic_file,"w+")
            lic.write(lic_str)
            lic.close()
            self.encode_file()

        except Exception,e:
            logging.error("fatal error run():" + str(e))


if __name__ == "__main__":

    chanllage_code = "xcdSq2+UbuIvtXuHQlhx0vnhGka+mRdfghTG1ktAq9RRQYD6cKU6GTEXNHiGEQ4hetG+PfuvyONtvsLrD0MpC4px7OeYQ8FD1VPNnAyCS0O1GvFBPRFz7h2w33xuBsEmIjnKv2Ta398d3cFFnodVkXzsAi1E8Xr2jvHgbMZQ+XPDcydW+GlSeZ73yzl9FSlgD8t7NwFESI0YluPxTbGH6CH2p0LYEIbkHKCJzHey1fk7qB0hfJnljYtVO0BEzaa8ThEH8XwyIpYLgYvtZBb/84/jpcHsloRzedlZ4PCRlvnihYZkP67QdqzTnBaGU+X99DWwT5iYNAiHcEQdg+RUlwA8FG0QRQ8/llFyoI4zZZXUQr4ilYO0onW1qfdcb6uPLTUfzr2NUyTcrAH4AEFGpwLsfAd7PEJWPTNAbU6gYNWK+yAI1F5VCCgnn/wJTazIHrk2M1n+gKRsChjB1NVoQ3KJaUwTRu4l3ACg1MfQVO+EQYfcw3hVgsFogYGK9Njn"

    print sys.getdefaultencoding()
    lic = LicenseManager("2017-06-19","2019-06-07","WAF0HW0B1A01","11111000,10110000,11001000,00000000",chanllage_code)
    lic.run()
    # verify_lic("/root/test_lic[WAF-2810][WAF0HW0B1A01][2018-06-07].lic")
    # ret = lic._verify_challenge_code(chanllage_code)
    # print ret
