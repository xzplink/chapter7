#!/usr/bin/env python
# -*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2016/11/28

import logging
import urllib
import urllib2
import re
import Queue
from threading import Thread

RAW_URL_FILE = "20161121"
SAVE_DIR   = "/root/tongguan_url/"
THREAD_NUM = 10
url_queue = Queue.Queue()

def reporthook(block_read,block_size,total_size):
    percent = 100.0 * block_read * block_size/total_size
    if percent > 100:
        percent = 100
    print "%.2f%%" % percent

def download_pdf1(url,filename,cb):
    try:
        urllib.urlretrieve(url,filename,reporthook=cb)
    except Exception,e:
        logging.error("download failed,"+ str(e))
#end def

def download_pdf2(url,sid,filename=None):
    ret = -1
    try:
        f = urllib2.urlopen(url, timeout=5)
        retcode = f.getcode()
        # print retcode
        info = f.info()
        # print info

        if filename == None:
            filename = str(sid) + ".pdf"

        if int(retcode) == 200:
            m = re.search(r'Content-Type:.*pdf',str(info))
            if m:
                data = f.read()
                with open(SAVE_DIR + filename,"wb") as code:
                    code.write(data)
                    ret = sid
        f.close()
        return ret
        #end if
    except Exception,e:
        logging.error("download failed," + str(e))
        return ret
#end def

def parse_raw_url(filename):
    ret_list = []
    idx = 0
    try:
        f = open(SAVE_DIR+filename, "r")
        for line in f.readlines():
            tuple_list = []
            tuple_list.append(idx + 1)
            tuple_list.append("http://" + line)
            # print tuple_list
            url_queue.put(tuple_list)
            idx = idx + 1
        #end for
    except Exception,e:
        logging.error("parser file error," + str(e))
    else:
        f.close()
#end def

def file_download_handler():
    while not url_queue.empty():
        queue_node = url_queue.get()
        # print queue_node
        download_pdf2(queue_node[1],queue_node[0])
        print "------------------"

    print "[*] this thread is end."
#end def

if __name__ == "__main__":
    # test_url="http://www.keepalived.org/pdf/sery-lvs-cluster.pdf"
    # file_name="raw_url.txt"

    #download_pdf1(test_url,file_name,reporthook)
    # download_pdf2(test_url,1)
    parse_raw_url(RAW_URL_FILE)
    try:
        list = []
        for i in range(THREAD_NUM):
            print "[*] Spawning thread: %d" % i
            list.append(Thread(target=file_download_handler))
        #end for
        for t in list:
            t.start()
        #end for

        for t in list:
            t.join()
            #end for
    except Exception,e:
        logging.error("start thread error," + str(e))
