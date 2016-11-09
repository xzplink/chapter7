#!/usr/bin/env python
#-*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2016/11/7

"""
--------User Manual----------
iptables -I INPUT -d 192.168.0.0/24 -j NFQUEUE --queue-num 1

apt-get install build-essential python-dev libnetfilter-queue-dev
pip install NetfilterQueue
or
wget http://pypi.python.org/packages/source/N/NetfilterQueue/NetfilterQueue-0.7.tar.gz
tar -xvzf NetfilterQueue-0.7.tar.gz
cd NetfilterQueue-0.7
python setup.py install
"""

from netfilterqueue import NetfilterQueue
import socket

def print_and_accept(pkt):
    print(pkt)
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)
try:
    nfqueue.run_socket(s)
except KeyboardInterrupt:
    print('')

s.close()
nfqueue.unbind()