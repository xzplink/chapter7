#!/usr/bin/env python
# -*-encoding:UTF8-*-
# Create by zhaozhang
# on 2017/02/17

import sqlite3
import sys
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

# logging.basicConfig(level=logging.info,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='translate.log',
#                     filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

print sys.getdefaultencoding()

RULES_DB_NAME = "/var/config/rules.db"
SOLU1_zh_CN = "目前厂商已经发布了升级补丁以修复这个安全问题，补丁下载链接"
SOLU2_zh_CN = "目前厂商已经发布了升级补丁以修复此安全问题，补丁获取链接"
SOLU3_zh_CN = "目前厂商已经发布了升级补丁以修复这个安全问题，请到厂商的主页下载"
SOLU4_zh_CN = "目前厂商还没有提供补丁或者升级程序，我们建议使用此软件的用户随时关注厂商的主页以获取最新版本"
SOLU5_zh_CN = "目前厂商还没有提供此漏洞的相关补丁或者升级程序，建议使用此软件的用户随时关注厂商的主页以获取最新版本"
SOLU6_zh_CN = "目前厂商已经发布了升级补丁以修复这个安全问题，\n补丁下载链接"
SOLU7_zh_CN = "目前厂商还没有提供此漏洞的相关补丁或者升级程序，建议使用此软件的用户随时关注厂商的主页以获取最新版本"
SOLU8_zh_CN = "目前厂商已经在最新版本的软件中修复了这些安全问题，请到厂商的主页下载"
SOLU9_zh_CN = "补丁获取链接"
SOLU10_zh_CN = "目前厂商还没有提供补丁或者升级程序，建议使用此软件的用户随时关注厂商的主页以获取最新版本"
SOLU11_zh_CN = "厂商目前已经发布了升级补丁以修复此安全问题，补丁获取链接"
SOLU12_zh_CN = "暂无数据"

SOLU1_en_US = "The current vendor has released an upgrade patch to fix this security issue, patch download link"
SOLU2_en_US = "The current vendor has released an upgrade patch to fix this security issue, patch access link"
SOLU3_en_US = "At present, these security issues have been fixed in the latest version of the software by the manufacturers, please go to the manufacturer's home page to download"
SOLU4_en_US = "At present, the manufacturer has not provided the patch or the upgrade procedure. We recommend that you pay attention to the manufacturer's home page to get the latest version"
SOLU5_en_US = "At present, the vendor has not provided the patch or upgrade procedure of this vulnerability. We recommended that you pay attention to the manufacturer's home page to get the latest version"
SOLU6_en_US = "The current vendor has released an upgrade patch to fix this security issue, patch download link"
SOLU7_en_US = "At present, the vendor has not provided the patch or upgrade procedure of this vulnerability. We recommended that you pay attention to the manufacturer's home page to get the latest version"
SOLU8_en_US = "At present, these security issues have been fixed in the latest version of the software by the manufacturers, please go to the manufacturer's home page to download"
SOLU9_en_US = "patch access link"
SOLU10_en_US = "At present, the vendor has not provided the patch or upgrade procedure of this vulnerability. We recommended that you pay attention to the manufacturer's home page to get the latest version"
SOLU11_en_US = "The current vendor has released an upgrade patch to fix this security issue, patch download link"
SOLU12_en_US = "No data yet"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def main():
    try:
        conn = sqlite3.connect(RULES_DB_NAME)
        conn.text_factory = str
        conn.row_factory = dict_factory
        cursor = conn.cursor()

        sql = "SELECT *FROM rules_internal WHERE solution_en_us is NULL;"
        cursor.execute(sql)
        results = cursor.fetchall()
        print "[*] get result done!"

        for i in results:
            solution = i['solution'].encode('utf-8')

            if solution.find(SOLU1_zh_CN) != -1:
                print "SOLU1:1111111111"
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    solution = SOLU1_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))

            elif solution.find(SOLU2_zh_CN) != -1:
                print "SOLU2:2222222222222"
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    # print "SOLU2:2222222222222"
                    # print solution
                    solution = SOLU2_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        # print "SOLU2:222222222"
                        # print solution
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))

            elif solution.find(SOLU3_zh_CN) != -1:
                print "SOLU3:3333333333"
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    # print "SOLU3:3333333333"
                    # print solution
                    solution = SOLU3_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        # print "SOLU3:33333333333"
                        # print solution
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))

            elif solution.find(SOLU4_zh_CN) != -1:
                print "SOLU4:4444444444"
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    # print "SOLU4:4444444444"
                    # print solution
                    solution = SOLU4_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        # print "SOLU4:4444444444"
                        # print solution
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))

            elif solution.find(SOLU5_zh_CN) != -1:
                print "SOLU5555555555555"
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    # print "SOLU5555555555555"
                    # print solution
                    solution = SOLU5_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        # print "SOLU5555555555555"
                        # print solution
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))

            elif solution.find(SOLU6_zh_CN) != -1:
                print "SOLU666666666"
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    # print "SOLU666666666"
                    # print solution
                    solution = SOLU6_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        # print "SOLU666666666"
                        # print solution
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))

            elif solution.find(SOLU7_zh_CN) != -1:
                print "SOLU77777777"
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    # print "SOLU77777777"
                    # print solution
                    solution = SOLU7_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        # print "SOLU777777"
                        # print solution
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))

            elif solution.find(SOLU8_zh_CN) != -1:
                print "SOLU8888888888"
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    # print "SOLU8888888888"
                    # print solution
                    solution = SOLU8_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        # print "SOLU8888888888"
                        # print solution
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))

            elif solution.find(SOLU9_zh_CN) != -1:
                print "SOLU9999999999"
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    # print "SOLU9999999999"
                    # print solution
                    solution = SOLU9_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        # print "SOLU99999999"
                        # print solution
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))

            elif solution.find(SOLU10_zh_CN) != -1:
                print "SOLU101010101010"
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    # print "SOLU101010101010"
                    # print solution
                    solution = SOLU10_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        # print "SOLU101010101010"
                        # print solution
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))


            elif solution.find(SOLU11_zh_CN) != -1:
                print "SOLU1+1+1====="
                # print solution
                idx = solution.find('http')
                if idx != -1:
                    # print "SOLU1+1+1====="
                    # print solution
                    solution = SOLU11_en_US + " : " + solution[idx:]
                    update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                    cursor.execute(update_sql,(solution, i['id']))
                else:
                    idx = solution.find('ftp')
                    if idx != -1:
                        # print "SOLU1+1+1====="
                        # print solution
                        solution = SOLU1_en_US + " : " + solution[idx:]
                        update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                        cursor.execute(update_sql,(solution, i['id']))

            elif solution.find(SOLU12_zh_CN) != -1:
                solution = SOLU12_en_US
                update_sql = "UPDATE `rules_internal` SET solution_en_us=? where id=?"
                cursor.execute(update_sql,(solution, i['id']))

        conn.commit()

        cursor.close()
        conn.close()
    except Exception,e:
        logging.error("main error," + str(e))

if __name__ == "__main__":
    main()
    # str = """目前厂商已经发布了升级补丁以修复这个安全问题，请到厂商的主页下载：http://www.trendmicro.com/download/product.asp?productid=5"""
    # idx =  str.find("http")
    # if idx != -1:
    #     print idx
    #     print str[idx:]