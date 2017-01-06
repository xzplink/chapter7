#!/bin/bash
# Put this file to /var/waf/waf
# and add start up command in rc.local
# Create by zhaozhang@yxlink.com
# On 2017/01/05

SSH_CONF=/etc/ssh/sshd_config
APACHE2_CONF=/etc/apache2/ports.conf
NIC_CONF=/etc/waf_nic.conf
WAF_CONF=/var/waf/waf.conf

[ -e $SSH_CONF ] || exit 0
[ -e $APACHE2_CONF ] || exit 0

###### 1、Update ssh config ##############
/bin/sed -i '/ListenAddress/d' ${SSH_CONF}
/bin/sed -i '/Port/a\ListenAddress 0.0.0.0' ${SSH_CONF}

###### 2、Update apache config ##############
/bin/sed -i '/:443/d' ${APACHE2_CONF}
/bin/sed -i '/ssl.c/a\Listen *:443'  ${APACHE2_CONF}

###### 3、Get basic config info #############
ADDR=$(ifconfig eth2|grep 'inet addr:'|awk '{print $2}')
if [ -z $ADDR ]; then
    echo "eth2 don't get ip address from dhcp server."
    exit 0
fi

IP=${ADDR##*:}
GATE_WAY=${IP%.*}
GATE_WAY=${GATE_WAY}.1
ETH_NAME=$(grep 'eth2' $NIC_CONF)
ETH_NAME=${ETH_NAME%%=*}
DB_PASSWD=$(grep 'db_passwd' $WAF_CONF |awk '{print $3}'|tr -d '"')
SQL_FILE=/tmp/update_eth2.sql
echo "use waf_hw;update net_config set Ip='$IP',Gateway='$GATE_WAY' where Name='$ETH_NAME';" > $SQL_FILE

###### 4、Update eth2 IP to mysql #############
FAILURE=0
/usr/bin/mysql -uroot -p$DB_PASSWD -e "source $SQL_FILE"
FAILURE=$?
if [ $FAILURE -ne 0 ]; then
    echo "Error, update eth2 ip to mysql failure."
    /bin/rm $SQL_FILE
    exit 1
fi
echo "Well done, update eth2 ip to mysql successfull."
/bin/rm $SQL_FILE

exit 0



