#!/bin/bash 

/sbin/iptables -F
/sbin/iptables -P FORWARD DROP
/sbin/iptables -A FORWARD -p tcp -m multiport --ports 20,21 -j ACCEPT
/sbin/iptables -A FORWARD -p tcp --dport 1024: -m state --state ESTABLISHED,RELATED -j ACCEPT 
modprobe ip_nat_ftp >/dev/null 2>&1

exit 0

