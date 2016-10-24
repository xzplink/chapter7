#!/usr/bin/env python
#-*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2016/10/24

import os
import sys
import logging

raw_url_file_name = "/root/data_instance.txt"
all_url_lines = []
all_url_list = []


def parse_raw_data():
    global all_url_list
    try:
        fd = open(raw_url_file_name,"r")
        all_url_lines = fd.readlines()
    except Exception,e:
        logging.getLogger().error("open file %s error." % raw_url_file_name)
    else:
        fd.close()

    # try:
        line = 0
        for i in all_url_lines:
            if len(i) == len("\n"): # ignore empyt lines
                continue

            url_dic = {'accesstime':'','srcip':'','srcport':'','destip':'','destport':'','method':'','host':'',
                       'url':'','useragent':'','content':'','cookie':'','referrer':'','statuscode':'','contenttype':'',
                       'response':'','day':''}
            split_str = i.split("~#~")
            print split_str
            print len(split_str)
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
                all_url_list.append(url_dic)
            line = line + 1
        #end for
    # except Exception,e:
    #     logging.getLogger().error("parse_raw_data error in line[%d]." % line)

#end def

if __name__ == "__main__":
    parse_raw_data()
    # print all_url_list
#end if