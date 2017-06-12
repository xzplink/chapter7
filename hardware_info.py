#!/usr/bin/env python
# -*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2017/06/06

import sys
import base64
import json
import os, fcntl, struct
from Crypto.Cipher import AES

NET_70_FILE = "/etc/udev/rules.d/70-persistent-net.rules"

class PycryptoAES(object):
    _key = "vbglodckidapckcavbglodckidapckca"
    _iv = "eacpqkdckzefjalceacpqkdckzefjalc"

    def __init__(self,key=_key,iv=_iv[:16]):
        self.key = key
        self.iv = iv
        self.mode = AES.MODE_CBC
        self.BS = AES.block_size
        self.pad = lambda s: s + (self.BS - len(s) % self.BS)*chr(0)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self,text):
        try:
            text = self.pad(text)
            cryptor = AES.new(self.key,self.mode,self.iv)
            cipher_text = cryptor.encrypt(text)
            return base64.b64encode(cipher_text)
        except:
            return ""

    def decrypt(self,text):
        try:
            cryptor = AES.new(self.key,self.mode,self.iv)
            plain_text = cryptor.decrypt(base64.b64decode(text))
            return plain_text.rstrip('\0')
        except:
            return ""

class HardwareInfo(object):
    def __init__(self):
        self.core_num = self._cpu_core_number()
        self.hdisk_sernum = self._hardisk_serial_num()
        self.cpu_type = self._cpu_type()
        self.cpu_id = self._cpu_id()
        self.mb_uuid = self._motherboard_uuid()
        self.sys_time = self._system_now()
        self.mem_total = self._memory_total()
        self.mac_list = self._ether_mac_list()

    def _hardisk_serial_num(self):
        with open("/dev/sda", "rb") as fd:
            hd_driveid_format_str = "@ 10H 20s 3H 8s 40s 2B H 2B H 4B 6H 2B I 36H I Q 152H"
            HDIO_GET_IDENTITY = 0x030d
            sizeof_hd_driveid = struct.calcsize(hd_driveid_format_str)
            assert sizeof_hd_driveid == 512

            buf = fcntl.ioctl(fd, HDIO_GET_IDENTITY, " " * sizeof_hd_driveid)
            fields = struct.unpack(hd_driveid_format_str, buf)
            serial_no = fields[10].strip()
            # model = fields[15].strip()
            return serial_no

    def _cpu_core_number(self):
        try:
            ret = 0
            pip = os.popen("cat /proc/cpuinfo|grep pro|wc -l","r")
            if pip:
                ret = int(pip.read())
            pip.close()
            return ret
        except:
            return 0

    def _cpu_type(self):
        try:
            ret = ""
            pip = os.popen("cat /proc/cpuinfo|grep name|cut -f2 -d:|uniq -d","r")
            if pip:
                ret = str(pip.read()).strip()
            pip.close()
            return ret
        except:
            return ""

    def _cpu_id(self):
        try:
            ret = ""
            pip = os.popen("dmidecode -t processor|grep ID|cut -d: -f2","r")
            if pip:
                ret = str(pip.read()).strip()
            pip.close()
            return ret
        except:
            return ""

    def _motherboard_uuid(self):
        try:
            ret = ""
            pip = os.popen("dmidecode -s system-uuid","r")
            if pip:
                ret = str(pip.read()).strip()
            pip.close()
            return ret
        except:
            return ""

    def _system_now(self):
        try:
            ret = ""
            pip = os.popen("date +%Y%m%d","r")
            if pip:
                ret = str(pip.read()).strip()
            pip.close()
            return ret
        except:
            return ""

    def _memory_total(self):
        try:
            ret = 0
            pip = os.popen("free -m|grep Mem|awk '{print int($2/1000+0.99)}'","r")
            if pip:
                ret = int(pip.read())
            pip.close()
            return ret
        except:
            return ""

    def _ether_mac_list(self):
        try:
            ret = ""
            if os.path.exists(NET_70_FILE):
                pip = os.popen("ifconfig -a|grep 'HWaddr'|grep -v wafbridge|awk '{print $5}'|sort","r")
                if pip:
                    for i in pip.readlines():
                        if not ret:
                            ret = i.rstrip("\n")
                        else:
                            ret += "," + i.rstrip("\n")
                pip.close()
            return ret
        except:
            return ""

def get_text_md5(text):
    try:
        import hashlib
        md = hashlib.md5()
        md.update(text)
        md5sum = md.hexdigest()
        return md5sum
    except:
        return

def verify_hardware_info(md5):
    try:
        tmp_dic = {}
        hardware = HardwareInfo()
        tmp_dic["core_num"] = hardware.core_num
        tmp_dic["mem_total"] = hardware.mem_total
        tmp_dic["hdisk_sernum"] = hardware.hdisk_sernum
        tmp_dic["cpu_type"] = hardware.cpu_type
        tmp_dic["cpu_id"] = hardware.cpu_id
        tmp_dic["mb_uuid"] = hardware.mb_uuid
        tmp_dic["mac_list"] = hardware.mac_list

        dump_str = json.dumps(tmp_dic)
        md5sum = get_text_md5(dump_str)
        # print md5sum

        return cmp(md5sum, md5)
    except:
        return False

def get_user_info():
    return "测试专用"

def get_request_model_no():
    return "Yxlink WAF-5830"

def generator_challenge_code():
    try:
        info_dict = {}
        ret = ""
        hardware = HardwareInfo()
        info_dict["core_num"] = hardware.core_num
        info_dict["mem_total"] = hardware.mem_total
        info_dict["sys_time"] = hardware.sys_time
        info_dict["hdisk_sernum"] = hardware.hdisk_sernum
        info_dict["cpu_type"] = hardware.cpu_type
        info_dict["cpu_id"] = hardware.cpu_id
        info_dict["mb_uuid"] = hardware.mb_uuid
        info_dict["mac_list"] = hardware.mac_list
        info_dict["user"] = get_user_info()
        info_dict["modelno"] = get_request_model_no()

        if info_dict:
            cryptor = PycryptoAES()
            dump_str = json.dumps(info_dict)
            print dump_str
            ret = cryptor.encrypt(dump_str)
        return ret
    except:
        return ""



if __name__ == '__main__':

    if os.geteuid() >  0:
        print("ERROR: Must be root to user")
        sys.exit(1)


    challenge_code = generator_challenge_code()
    print challenge_code
    verify_hardware_info(challenge_code)

