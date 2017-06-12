#!/usr/bin/env python
# -*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2017/06/07

import rsa
import sys
import json
import string
import random
import logging


# reload(sys)
# sys.setdefaultencoding('utf8')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s')

public_key_str = """-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAJ6m+aWR00650XWRNzAcy2ywCS5UAyPC4RVhlAP0BOtjegv5rHFgs/Wg
C+lHUCwQ6/vnS9uebcnlSCjldMQRqGLoCyHdvuN0USWBRsJkCsYXWNEuoiwZ3RUQ
EJuhGBjhy7bAN80SqTIUoPgMSfHCe1ymi3ppuskAOTfOR3KjhvlFAgMBAAE=
-----END RSA PUBLIC KEY-----"""

private_key_str = """-----BEGIN RSA PRIVATE KEY-----
MIICYQIBAAKBgQCepvmlkdNOudF1kTcwHMtssAkuVAMjwuEVYZQD9ATrY3oL+axx
YLP1oAvpR1AsEOv750vbnm3J5Ugo5XTEEahi6Ash3b7jdFElgUbCZArGF1jRLqIs
Gd0VEBCboRgY4cu2wDfNEqkyFKD4DEnxwntcpot6abrJADk3zkdyo4b5RQIDAQAB
AoGAHQciEEgxKGtZRrCOL3BlS/qdg2t9s5JZiobzBRIlwEfQMda51XjDFIL3CvSw
V4+1Db8RIxrGrbUU0d7Bsj2r9l31jCcZvf3ohqRklcWZ/OF7ndL1pHq1yOR3jqVY
JcVie7OZmAt6dqT7FqzbapdxoU5tMmILI9hQBhwhC+puXPUCRQCrD6APLQvgioTK
kkh3iaMBgH/sU2aRk50q7kQhS8XIs1G3tJihBxveXKkflllW/Nxr6EDKBDgmvzEr
SVeNOZGdXZ13lwI9AO1uAp+QopQ6nmsYCApCihnVCJ8hcvERokm9Wgcadfr/fW9d
HwDdCB/YKDwNHTObExhyERBeo1TMo0RRgwJEP5PxI3LUpUIWlMvFz1gCk75UzVs6
FgVNNvWTsORewHeVebfPupnPy9eYrDrPPbuBmUGbQvpKfGw3NCVwOvcYnep7akUC
PQCSb1sm1qmvCkhSfMvYqBlMvVtH6fVeQSX6nNI9t1A0sgbG/IP2oFw2Z7bI8r2j
6mzoktF7ayMJVf0MUckCRQCJPNzi+INd9rXghnDIpx49gMML719k8fkLlpwOD2Se
8PKB5W18W0u8ECrHS906JZFESKLqVYWqmM2jgBVTOp7XzdjWfA==
-----END RSA PRIVATE KEY-----"""

n=24625762657381141107391324296405776455871493080169289352871061194703831990558940603860568035064346462503773208074622392521378141587419770580777682193039448118520007206712288501389159549751661455425547103638215421575277064597083636896488951924661389291435841129055261450437407323316389362866209404724449679830565018861561567847070203602770001230431948952518314307113269292224867396135186763033871990312980368872077752917729644891556065348020379930830055642272557579818964365882147113643668880872274396803803559263709930177895758475604313325202146777967056551432199187168178015562902377679105727797512766125901244241869
d=1690003319624195958350385000733729756775494623148872798726445376107125724842280237519842904367161031740455024083552517133820068540313121510445527209326236635584706376931235485389452125963349315568419899269289293637519014237054759394857084936006173774902459685327321864245704424149163975882975155226187723125605425991844840054298343382746368003059036594961263030255636255108236005503285064013238614286231601684052880698424252633961257570232301470378816050766687000834551394143440515101115039116074834793601335269657114509198898425006226212425769161758502160872942379528364231474622506400702556835798438570560584763873
e=17
p=167551891611585131795348220561903349482214995415826520821102562207453771788966095174465148052395555658664564159294745394481093521737508835217138461473810849552451430130804735779497942776017832910979033795849328777011033213747488883872341301749439958927779231448565330427167953332667726201902765913252750454841.
q=146973945925170495498994662189592693518057859095512202567181298440260401298352592237929891232638617245785498581395789687925218660040763955807311869627021860963049763946923443533637510976308971186062211538571218552557919640337528203125740547736585105498688139734876740791235045364772173416832752470194258656309.


HDMODE = [[1210, 1220, 2820], [5830, 6830, 5930, 6930], [8900, 8930]]
HDWARE_CONF = {}

class PycryptoRSA(object):
    (_crt, _key) = rsa.newkeys(1024)

    # _key = rsa.PrivateKey.load_pkcs1(private_key_str)
    # _crt = rsa.PublicKey.load_pkcs1(public_key_str)
    print _crt
    print _key

    def __init__(self, crt=_crt, key=_key):
        self.pubkey = crt
        self.privkey = key
        self._replace()
        print self.pubkey
        print self.privkey

    def _replace(self):
        self.pubkey.n = self.privkey.n = n
        self.pubkey.e = self.privkey.e = e
        self.privkey.d = d
        self.privkey.p = p
        self.privkey.q = q

    def encrypt(self, text):
        try:
            cipher_text = rsa.encrypt(text, self.pubkey)
            logging.debug("cipher_text: %s" % cipher_text)
            return cipher_text
        except Exception,e:
            logging.error( "fatal error encrypt():" + str(e))
            return ""

    def decrypt(self, text):
        try:
            plain_text = rsa.decrypt(text, self.privkey)
            logging.debug("plain_text: %s" % plain_text)
        except Exception,e:
            logging.error("fatal error decrypt():" + str(e))
            return ""


class LicenseManager(object):
    _random_len = 16
    _lic_name = "/yxlink.lic"

    def __init__(self,begin,end,serno,feature,code,type=2):
        self.lic_rsa = PycryptoRSA()
        self.company = ""#"测试专用[2017-06-07]"
        self.license_type = type
        self.license_begin = begin#"2017-06-07"
        self.license_end = end#"2017-06-07"
        self.model = ""#"Yxlink WAF-2810"
        self.serial_num = serno#"WAF0HW0B1A01"
        self.random = self.random_generator()
        self.feature_set = feature#"11111000,10110000,11001000,00000000"
        self.hdmd5 = ""#"cc2c80528f80492b577507c33e77994c"
        self.code = code
        self.lic_file = sys.path[0] + self._lic_name

    def random_generator(self):
        field = string.letters + string.digits
        return "".join(random.sample(field, self._random_len))

    def _verify_lic(self, file_name=None):
        try:
            plain_lic = ""
            if file_name:
                file_path = file_name
            else:
                file_path = self.lic_file

            with open(file_path,"r") as lic:
                lic_content = lic.read()
                if lic_content:
                    plain_lic = self.lic_rsa.decrypt(lic_content)
                logging.debug("plain_lic: %s" % plain_lic)
            return plain_lic

        except Exception,e:
            logging.error("fatal error verify():" + str(e))

    def _verify_challenge_code(self):
        global HDWARE_CONF
        from hardware_info import PycryptoAES
        lic_aes = PycryptoAES()

        try:
            plain_text = lic_aes.decrypt(self.code)
            HDWARE_CONF = json.loads(plain_text)
            logging.debug("HDWARE_CONF: %s" % HDWARE_CONF)

            if HDWARE_CONF and len(HDWARE_CONF) != 10:
                return 1

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
        if HDWARE_CONF:
            self.hdmd5 = get_text_md5(HDWARE_CONF)

        if HDWARE_CONF["user"]:
            self.company = HDWARE_CONF["user"]

        if HDWARE_CONF["modelno"]:
            self.model = HDWARE_CONF["modelno"]

        if HDWARE_CONF["modelno"] and self.serial_num:
            model = str(HDWARE_CONF["modelno"]).split(' ')[1]
            file_name = "%s[%s][%s][%s].lic" % (HDWARE_CONF["user"], model, self.serial_num, self.license_end)
            print file_name
            # file_name = file_name.decode()
            self.lic_file = sys.path[0] + "/" + file_name
            # self.lic_file = self.lic_file.decode('utf8')
            logging.debug("lic_file is: %s" % self.lic_file)

    def run(self):
        self._prepare()
        try:
            lic_str = self.company + "\n"
            lic_str += self.license_type + "\n"
            lic_str += self.license_begin + "\n"
            lic_str += self.license_end + "\n"
            lic_str += self.model + "\n"
            lic_str += self.serial_num + "\n"
            lic_str += self.random + "\n"
            # lic_str += self.feature_set + "\n"
            # lic_str += self.hdmd5 + "\n"
            logging.debug("lic_str:%s \nlic_str len:%d" %(lic_str, len(lic_str)))
            lic_str = lic_str.encode('utf8')
            cryptor_text = self.lic_rsa.encrypt(lic_str)

            with open(self.lic_file,"w+") as lic:
                lic.write(cryptor_text)

        except Exception,e:
            logging.error("fatal error run():" + str(e))

if __name__ == "__main__":
    test_str = """
测试专用[2017-06-07]
Yxlink WAF-2810
WAF0HW0B1A01
58ec519a5561a4a8"""

    myrsa = PycryptoRSA()
    cipher_text = myrsa.encrypt(test_str)
    plain_text = myrsa.decrypt(cipher_text)

    # chanllage_code = "nxR75C2G1A7nDn8BgKHHwYSrx3WuFNDpRSK6vvjFWvFmOOrQKHDBvLlPjKvAbelXjHuRiEsBYfvk3zjEXqdLp9RXcQ3Navtz82s5uRrJXYwHzsEWRLYi+XNduHRGYfea9azPJB2928ioGT5cPGEJNNlHtJHqARZJCY1hKVTzbHHobP9TmMJ+G1ea5jkPJTrpYDJVAkaw7WEPSsn+6oUasO4QTVql5gEVDQ8mVPij47jJOdIA+baxSAvcIpIUzQYQG9/LdGAZf86vP73vxjoUCAsRs4Yp2HFRIVS65U2Jv9KkGitDxJ3YAdEDV3l+GZBskCQNgOi+dZz8hP9J39oOKBfI/EjMg66aCZn6pxcCTCWCmCnEZwLN+3PxIpPxW2NHmNejGfeV7QkR+x1VXyybap2cnuh4JuUUBxpdrogCkjxEscD27KL5yBJcbe5N6Q8d++P8xOyYamPv8agpvnkdait65a7IufvqhM+MLfzXD8bM55osTic6RZ2jZ9oQTl2mHIuNfp6JczujfYenLZp4xgNSyy8Xn15NEaNbrJwZgv74DZpmX3yQeCUg+KdNSSXA"
    # from hardware_info import get_text_md5
    # get_text_md5(chanllage_code)
    # print sys.getdefaultencoding()
    # lic = LicenseManager("1","2017-06-09","2018-06-07","WAF0HW0B1A01","11111000,10110000,11001000,00000000",chanllage_code)
    # lic.run()
    # lic._verify_lic()
    # ret = lic._verify_challenge_code(chanllage_code)
    # print ret