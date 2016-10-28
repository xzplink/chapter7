#!/usr/bin/env python
#-*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2016/10/24

import os
import sys
import logging
import Queue
from threading import Thread
import requests

raw_url_file_name = "c:\data_instance.txt"
log_webshell_url = "/root/webshll_url.txt"
threads = 10
url_queue = Queue.Queue()

def parse_raw_data(file):
    global url_queue
    all_url_lines = []

    try:
        fd = open(file,"r")
        all_url_lines = fd.readlines()
    except Exception,e:
        logging.error("open file data_instance.txt error." + str(e))
    else:
        fd.close()

    try:
        num = 0
        for line in all_url_lines:
            line = line.strip("\r\n")

            if len(line) > 0:
                url_dic = {'accesstime':'','srcip':'','srcport':'','destip':'','destport':'','method':'','host':'',
                           'url':'','useragent':'','content':'','cookie':'','referrer':'','statuscode':'',
                           'contenttype':'','response':''}
                split_str = line.split("~#~")
                if len(split_str) > 0:
                    url_dic['accesstime'] = split_str[0]
                    url_dic['srcip']      = split_str[1]
                    url_dic['srcport']    = split_str[2]
                    url_dic['destip']     = split_str[3]
                    url_dic['destport']   = split_str[4]
                    url_dic['method']     = split_str[5]
                    url_dic['host']       = split_str[6]
                    url_dic['url']        = split_str[7]
                    url_dic['useragent']  = split_str[8]
                    url_dic['content']    = split_str[9]
                    url_dic['cookie']     = split_str[10]
                    url_dic['referrer']   = split_str[11]
                    url_dic['statuscode'] = split_str[12]
                    url_dic['contenttype']= split_str[13]
                    url_dic['response']   = split_str[14]
                    url_queue.put(url_dic)
                num = num + 1
            #end if
        #end for
    except Exception,e:
        logging.error("parse_raw_data error %s,in line[%d]." % (str(e),num))

#end def

def checkWebShell(content):
    try:
        if content and len(content) < 5000 and content.find('form') > 0 and content.find('input') > 0:
            form_content = ""
            other_content = ""
            if content.find('body') > 0:
                match = re.findall(r"<(\s*)body(.*?)>(.*?)<(\s*)form(.+?)>(.+?)<(\s*)/(\s*)form(\s*)>(.*?)<(\s*)/(\s*)body(\s*)>",content,re.I|re.DOTALL)
                if len(match) == 1:
                    form_content = match[0][5]
                    other_content = match[0][2] + match[0][9]
            else:
                match = re.findall(r"(\s*)(.*?)(\s*)<(\s*)form(.+?)>(.+?)<(\s*)/(\s*)form(\s*)>(\s*)(.*?)(\s*)",content,re.I|re.DOTALL)
                if len(match) == 1:
                    form_content = match[0][5]
                    other_content = match[0][1] + match[0][10]

            match = re.findall(r"<(\s*)input(.+?)type(\s*)=(\s*)(\"|')?(text|password)(\5)?(.+?)>",form_content,re.I|re.DOTALL)

            if match and len(other_content) < 50:
                return True

            match = re.findall(r"<(\s*)input(.+?)type(\s*)=(\s*)(\"|')?(text|password)(\5)?(.+?)>",content,re.I|re.DOTALL)
            if match:
                if content.find('window.onerror=killErrors;function yesok(){if (confirm') > 0 and content.find('top.hideform.FName.value += "||||"+DName;}else if(FAction==') > 0:
                    return True
        #end if (content <5000)
        else:
            if re.search(r"[^0-9.](10|172|192)\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])[^0-9.]",content,re.DOTALL) and re.search(r"<(\s*)input(.*?)type(\s*)=(\s*)(\"|')?(file|text)(\5)?(.+?)>",content) and re.search(r"[rwx-]{9}",content,re.I):
                return True

        return False
    except Exception,e:
        logging.error("File:WehShellCheckScript.py, checkWebShell function :" + str(e))
        return False
        #end try
#end def

def my_http_request():
    while not url_queue.empty():
        url_dic = url_queue.get()
        url = "http://" + url_dic['host'] + url_dic['url']
        # print url
        response = ''
        if url_dic['method'] == "GET":
            if url_dic['cookie'].strip(' '):
                headers = {'Host':'','Cookie':'','User-Agent':'','Referer':''}
                headers['Host']       = url_dic['host']
                headers['User-Agent'] = url_dic['useragent']
                headers['Cookie']     = url_dic['cookie']
                # headers['Referer']    = url_dic['referrer']
                # print headers
                response = requests.get(url,headers=headers)
            else:
                response = requests.get(url)
            print response.text

        elif url_dic['method'] == "POST":
            payload = ''
            if url_dic['content'].strip(' '):
                payload = url_dic['content']
                # print payload
            response = requests.post(url,data=payload)
            # print response.text

        if(response and response.status_code == requests.codes.ok):
            if checkWebShell(response.text) == True:
                os.system("echo %s >> log_webshell_url" % url)
    #end while
    print "[*] this thread is end."

#end def

if __name__ == "__main__":
    parse_raw_data(raw_url_file_name)

    try:
        list = []
        for i in range(threads):
            print "Spawning thread: %d" % i
            list.append(Thread(target=my_http_request))
        #end for
        for t in list:
            t.start()
        #end for

        for t in list:
            t.join()
        #end for
    except Exception,e:
        logging.error("start thread error," + str(e))
#end if