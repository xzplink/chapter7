#!/usr/bin/env python
# -*-coding:UTF-8-*-
# Create by zhaozhang@yxlink.com
# On 2016/12/8

import sys
import logging
import os
import subprocess
import time

def waf_popen(cmd):
    logging.getLogger().debug(cmd)
    p = subprocess.Popen(cmd,shell=True,close_fds=True,bufsize=-1,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    p.wait()
    return p.stdout.readlines()
#end def

try:
    while True:
        ports = []
        port_list = waf_popen("cat /proc/net/nf_conntrack|grep dport=21|awk '{print $9}'")
        for i in port_list:
            res = i.split("=")
            if res and len(res) > 0:
                ports.append(str(int(res[1]) + 1))
        #end for
        # print ports
        if ports:
            port_str = ",".join(ports)
            # print port_str
            ipt = "iptables -F; iptables -A FORWARD -p tcp --sport 21 -j ACCEPT; iptables -A FORWARD -p tcp --dport 21 -j ACCEPT;"
            extend = "iptables -A FORWARD -p tcp -m multiport --ports %s -j ACCEPT;" % port_str
            default = "iptables -A FORWARD -p tcp -j DROP"
            os.system(ipt + extend + default)
        time.sleep(1)
    #end while
except Exception,e:
    logging.error("dynamic_ftp error," + str(e))

