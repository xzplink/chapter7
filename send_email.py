#!/usr/bin/env python
# -*-coding:UTF-8-*-
# On 2016/11/30

import smtplib
import os
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication

sender = 'zhaozhang@yxlink.com'#发件人地址
receiver = 'zhaozhang@yxlink.com'#收件人地址
smtpserver = 'smtp.yxlink.com'#邮件服务器
username = 'zhaozhang'#用户名
password = 'r&b4537063'#密码
smtp = smtplib.SMTP()

def send_email(msg,file_name):
    print msg
    print file_name
    msgRoot = MIMEMultipart('related')
    msg = unicode(msg,"utf-8")
    msg = msg.encode("gb2312")
    # if not isinstance(msg,unicode):
    #     msg = unicode(msg,"UTF-8")
    #     print msg
    # file_name = file_name.encode("gb2312")

    msgRoot['Subject'] = msg#邮件标题，这里我把标题设成了你所发的附件名
    # print "Subject:%s" % msg.decode('utf-8')
    msgText = MIMEText('%s' % msg,'html','gb2312')#你所发的文字信息将以html形式呈现
    # msgText["Accept-Language"] = "zh-CN"
    # msgText["Accept-Charset"] = "ISO-8859-1,utf-8"
    # print "msgText:",msgText
    msgRoot.attach(msgText)
    att = MIMEText(open('%s'%file_name, 'rb').read(), 'base64', 'gb2312')#添加附件
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="%s"'% os.path.basename(file_name.encode("gb2312"))
    # print "basename:",os.path.basename(file_name)
    msgRoot.attach(att)
    count = 0
    while 1:#持续尝试发送，直到发送成功
        try:
            print "[*] begin to send email."
            smtp.sendmail(sender, receiver, msgRoot.as_string())#发送邮件

            print "[*] loop %d time again." % (count + 1)
            count = count + 1
            break
        except:
            try:
                smtp.connect(smtpserver)#连接至邮件服务器
                smtp.login(username, password)#登录邮件服务器
                print "[*] try connect to email server."
            except:
                print "failed to login to smtp server"#登录失败

if __name__ == "__main__":
    MSG="测试程序test"#要发送的文字
    # print MSG
    FILE=u"D:/测试suricata-0.8.0.tar.gz"#要发送的文件
    send_email(MSG,FILE)
    # try:
    #     send_email(MSG,FILE)
    # except Exception,e:
    #     logging.error("send email error," + str(e))
