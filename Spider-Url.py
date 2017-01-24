#!/usr/bin/env python
# -*-coding:UTF-8-*-
# Create by zhaozhang@yxlink.com
# On 2017/01/09

import logging
import urllib
import urllib2
import MySQLdb
import re
import Queue
import time
from threading import Thread

URL_QUEUE = Queue.Queue()
RESULT_LIST = []
HOST = "192.168.99.27"
DB_USER = "root"
DB_PASSWD = "yxserver"
DB_NAME = "waf_hw"
THREAD_NUM = 1
SUCCESS_COUNT = 0

def update_url():
    global RESULT_LIST
    try:
        conn = MySQLdb.connect(HOST, DB_USER, DB_PASSWD , db = DB_NAME, charset = "utf8")
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        # for i in range(len(RESULT_LIST)):
        #     sql = ("update vul_info set ref =%(url_new)s where ref =%(url)s;")
        #     data = {'url_new':'%s', 'url':'%s'}  % (RESULT_LIST[1], RESULT_LIST[0])
        #     # cursor.execute(sql, data)
        #     # conn.commit()
        #     print "sql:",sql
        #     print "data:",data

        if RESULT_LIST:
            sql = "use `waf_hw`;SET FOREIGN_KEY_CHECKS=0;SET autocommit=0;START TRANSACTION;"
            for i in RESULT_LIST:
                sql += "update vul_info set ref =\'%s\' where ref =\'%s\';" % (i[1], i[0])
            sql += "COMMIT;SET autocommit=1;"
            # print "sql:",sql
            cursor.execute(sql)
            conn.commit()
            print "[*] update url successfull"

        cursor.close()
        conn.close()
    except Exception,e:
        logging.error("update_url failed," + str(e))

def get_url():
    global URL_QUEUE
    try:
        conn = MySQLdb.connect(HOST, DB_USER, DB_PASSWD , db = DB_NAME, charset = "utf8")
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        sql = "select id,ref,ref_cn from vul_info_bak where ref like '%nessus%';"
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()

        count = 0
        for row in res:
            split_url = row["ref"].split("\n")
            # print split_url
            for i in range(len(split_url)):
                if split_url[i].find("nessus") != -1:
                    # print split_url[i]
                    count = count + 1
                    URL_QUEUE.put(split_url[i])
        print "[*] url count is :%d" % count
        print "[*] get url successfull."

    except Exception,e:
        logging.error("get_url failed," + str(e))

def spider_url(url):
    global RESULT_LIST,SUCCESS_COUNT

    try:
        headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
        }
        request = urllib2.Request(url, headers=headers)
        f = urllib2.urlopen(request, timeout=5)
        retcode = f.getcode()
        print retcode
        info = f.info()
        # print info

        if int(retcode) == 302:
            get_url = f.geturl()
            m = re.search(r'Location:',str(info))
            if m:
                real_url = info.getheader("Location")
                if real_url.find("tenable") != -1 or real_url.find("nessus") != -1:
                    print "real_url:%s, spider it again." % real_url
                    spider_url(real_url)
                else:
                    tmp_list = []
                    tmp_list.append(url)
                    tmp_list.append(real_url)
                    RESULT_LIST.append(tmp_list)

        elif int(retcode) == 301:
            get_url = f.geturl()
            m = re.search(r'Location:',str(info))
            if m:
                real_url = info.getheader("Location")
                if real_url.find("tenable") != -1 or real_url.find("nessus") != -1:
                    print "real_url:%s, spider it again." % real_url
                    spider_url(real_url)
                else:
                    tmp_list = []
                    tmp_list.append(url)
                    tmp_list.append(real_url)
                    RESULT_LIST.append(tmp_list)
        elif int(retcode) == 200:
            get_url = f.geturl()
            print "get_url:",get_url
            if get_url.find("tenable") != -1 or get_url.find("nessus") != -1:
                pass
            else:
                tmp_list = []
                tmp_list.append(url)
                tmp_list.append(get_url)
                RESULT_LIST.append(tmp_list)
                SUCCESS_COUNT += 1
        else:
            print "bad url, pass it."
            return
    except Exception,e:
        print "[*] spider url is :%s" % url
        logging.error("spider_url failed," + str(e))
        return -1

def spider_url_handler():
    while not URL_QUEUE.empty():
        url = URL_QUEUE.get()
        # print url
        spider_url(url)
        time.sleep(0.5)
        # if SUCCESS_COUNT >= 2:
        #     break

    print "[*] this thread is end."
#end def

if __name__ == "__main__":
    # test_url="http://www.nessus.org/u?0d043d1b"
    # spider_url(test_url)

    """step 1: get url from mysql"""
    get_url()

    """step 2: spider url from internet"""
    try:

        list = []
        for i in range(THREAD_NUM):
            print "[*] Spawning thread: %d" % i
            list.append(Thread(target=spider_url_handler))

        for t in list:
            t.start()

        for t in list:
            t.join()

    except Exception,e:
        logging.error("start thread error," + str(e))

    """step 3: update url to mysql"""
    update_url()
    print "success update url count is :%d" % SUCCESS_COUNT