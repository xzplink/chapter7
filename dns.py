#-*-encoding:UTF-8-*-
import sys
# import MySQLdb
import os
import re
import urllib2
import random
import socket 
# import BeautifulSoup
# from BeautifulSoup import BeautifulSoup
import urllib
import time
import json
import cookielib
# from mod_python import apache
import logging
import struct
reload(sys)
sys.setdefaultencoding('utf-8')

def initLog():
    logging.basicConfig(
            filename = 'dns.log',
            filemode = 'a',
            format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
            datefmt = '%a, %Y-%m-%d %H:%M:%S',
            level = logging.DEBUG,
            )



host = "127.0.0.1"#"192.168.9.32"
user = "root"
passwd = "yxserver"


# class domain_info(object):
#     def __init__(self, d, t):
#         self.domain = d
#         self.title  = t
#     #end def
# #end class

def get_url_content(url,timeout, proxy_str = None):
    
    try:
        if url == "":
            return None
        #end if
        
        url = url.replace(' ','')
        if url.lower().find('http://') < 0:
            url = 'http://' + url     
        #end if
        
        if url != '':
            socket.setdefaulttimeout(timeout)
            #proxy_str = '192.168.9.74:8080'
            if proxy_str != None:
                
                proxy_support = urllib2.ProxyHandler({'http':proxy_str})  
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)  
                #urllib2.install_opener(opener)
                #logging.debug('urlp:'+url)
                f = opener.open(url)
            else:
                #logging.debug('url:'+url)
                f = urllib2.urlopen(url)
            #end if
            
            
            if f:
                html = f.read()
                #print html
                f.close()
                #logging.debug('html:'+ str(len(html)))
                return html
            else:
                return None
            #end if
        else:
            return None
        #end if
        
    except Exception,e:
        #print e
        logging.error('error proxy:'+str(e))
        return None
    #end try
#end def


# def g2u(mystr):
#     try:
#         return mystr.decode('UTF-8').encode(sys.getfilesystemencoding())
#     except Exception,e:
#         print e
#         return ''
#     #end try
# #end def

# def get_ip_by_host(domain):
#     try:
#         ip = ''
#         ip = socket.gethostbyname(domain)
#         return ip
#     except Exception,e:
#         return ''
#     #end try
# #end def

# def getUrlEncode (url, timeout):
#     try:
#         if url == '':
#             return ''
#         #end if
#
#         if url.lower().find('http://') < 0:
#             url = 'http://' + url
#         #end if
#
#         charset_str = ""
#         #html = urllib.urlopen(url)
#         socket.setdefaulttimeout(timeout)
#         f = urllib2.urlopen(url)
#         f.close()
#
#         if f != '':
#             header = f.headers['Content-Type']
#             flag = True
#             if header.find('charset') and flag:
#                 header = header + "#"
#                 m_charset = re.search('charset=([\w\d-]+?)#',header,re.I)
#                 if m_charset:
#                     charset_str = m_charset.group(1)
#                     flag = False
#                 #end if
#             #end if
#             if flag:
#                 content = f.read()
#                 m_charset = re.search('<meta.*.charset=([\w\d-]+?)"', content.decode("ISO-8859-1"), re.IGNORECASE)
#                 if m_charset:
#                     charset_str = m_charset.group(1)
#                     flag = False
#                 #end if
#             #end if
#             if flag:
#                 content = html.read()
#                 m_charset = re.search('<meta.*.charset="([\w\d-]+?)"', content.decode("ISO-8859-1"), re.IGNORECASE)
#                 if m_charset:
#                     charset_str = m_charset.group(1)
#                     flag = False
#                 #end if
#             #end if
#             if flag or charset_str == "":
#                 charset_str = "gb2312"
#             #end if
#         else:
#             charset_str = ''
#         #end if
#         return charset_str
#     except Exception,e:
#         #logging.error("get url encode Exception(GetDomainThread):" + str(e))
#         return ''
#     #end try
# #end def
#
# def get_title_by_url(url):
#     try:
#         if url == "":
#             return ""
#         #end if
#
#         title = ""
#         url = url.replace(' ','')
#         if url.lower().find('http://') < 0:
#             url = 'http://' + url
#         #end if
#
#         charset = getUrlEncode(url, 10)
#         #print charset
#         if charset.find("gb") >= 0 or charset.find("GB") >= 0:
#             soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url),fromEncoding="gbk")
#         else:
#             soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url))
#         #end if
#
#         if soup.title:
#             titleTag = soup.title
#             if titleTag and titleTag.string:
#                 titlestring = titleTag.string
#                 title = titlestring.strip()
#                 return title
#             else:
#                 print 1
#                 return ''
#             #end if
#         else:
#             print 2
#             return ''
#         #end if
#     except Exception,e:
#         #logging.error("get title by url Exception(GetDomainThread)(task_id:" + str(self.taskId) + "):" + str(e))
#         print "get_title_by_url", e
#         return ''
#     #end try
# #end def

# def getdomains(url_content,ip):
#     ret_domains = []
#     tmp_domains = []
#     try:
#
#         count_i = 0
#         ss = url_content
#         urls = re.findall(r"<a.?.href=\"http://.*?<\/a>",ss,re.I)
#         #print urls
#
#
#         for i in urls:
#
#             if i.find("bing")>0 or i.find("live.com")>0 or i.find("microsoft.com")>0 or i.find("msn.com")>0 or i.find("www.microsofttranslator.com")>0:
#                 continue
#             #end if
#             #tmp_title = re.findall(r"http://.*.\"",i,re.I)
#             aaa = re.findall(r"http://.*.\"",i,re.I)
#
#             ccc = re.findall(r"\">(.*?)</a>",i,re.I)
#
#             #ccc = re.findall(r"\)\">.*.<\/a>",i,re.I)
#             if len(aaa)>0:
#
#                 #print aaa
#                 bbb = aaa[0].replace("/\"","")
#                 #print bbb
#                 bbb = bbb.replace("http://","")
#                 #print bbb
#                 bbb = bbb.replace("https://","")
#                 bbb = bbb.split('/')[0]
#                 #print bbb.split('/')
#                 bbb = bbb.split(" ")[0]
#                 #print bbb
#                 #print "================"
#                 fff = ""
#                 if len(ccc) > 0:
#                     fff = ccc[0].replace(")\">","")
#                     fff = fff.replace("</a>","")
#                 else:
#                     fff = bbb
#                 #end if
#
#                 if  True:
#                     ip = g2u(ip)
#                     if ip == get_ip_by_host(bbb) :
#                         #print "insert domain list,domain:",bbb," ip:",ip
#
#                         if bbb not in tmp_domains:
#                             ret_domains.append(domain_info(bbb, fff))
#                             tmp_domains.append(bbb)
#
#
#                         """
#                         if self.mysqlConnect():
#                             self.cursor.execute("insert into %s (`task_id`,`task_name`,`domain`,`ip`,`desc`,`status`,`start_time`,`end_time`,`first_page`,`high`,`med`,`low`,`count`,`process`,`processLabel`) values ('%s','%s','%s','%s','%s','1','0000-00-00 00:00:00','0000-00-00 00:00:00','%s','0','0','0','0','0','')" % (self.domain_list_table,self.taskId,self.task_name,bbb,ip,fff,''))
#                             count_i = count_i + 1
#                             self.conn.commit()
#                         else:
#                             logging.error("getdomains mysql connect error")
#                         #end if
#                         """
#                     #end if
#                 #end if
#             #end if
#             aaa=re.findall(r"http://.*.target=\"_blank\"",i,re.I)
#             ccc=re.findall(r"\)\">.*.<\/a>",i,re.I)
#         #end for
#         if count_i <= 0:
#             #print "insert into domain list,ip:",ip
#             """
#             if self.mysqlConnect():
#                 self.cursor.execute("insert into %s (`task_id`,`task_name`,`domain`,`ip`,`desc`,`status`,`start_time`,`end_time`,`first_page`,`high`,`med`,`low`,`count`,`process`,`processLabel`) values ('%s','%s','%s','%s','%s','1','0000-00-00 00:00:00','0000-00-00 00:00:00','%s','0','0','0','0','0','')" % (self.domain_list_table,self.taskId,self.task_name,ip,ip,ip,''))
#                 self.conn.commit()
#             else:
#                 logging.error("getdomains mysql connect error, can not inert IP : " + str(ip) + "(task_id:" + str(self.taskId) + ")")
#             #end if
#             """
#         #end if
#     except Exception,e:
#         print e
#     #end try
#     return ret_domains
# #end def

# def get_domain_by_ip(ip, req):
#
#     tmp_domains = []
#     d1= []
#
#     try:
#         conn = MySQLdb.connect(host, user, passwd, db='test', charset='utf8')
#         cur = conn.cursor(MySQLdb.cursors.DictCursor)
#
#         cur.execute("select * from proxy_list where total_failed = 0 and total_used > 0")
#         ret = cur.fetchall()
#         ret_len = len(ret)
#
#         try_times = 3
#
#         while try_times > 0:
#             #break
#             random_num = random.randint(0, ret_len)
#             proxy_ip   = ret[random_num]["ip"]
#             proxy_port = ret[random_num]["port"]
#
#             cur.execute("update `proxy_list` set `total_used` = %d where `id` = %d" \
#                         % (int(ret[random_num]["total_used"] + 1), int(ret[random_num]["id"]))
#                         )
#             conn.commit()
#
#             a = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n&first=1",10, "http://" + proxy_ip + ":" + str(proxy_port))
#
#             if a is None:
#                 cur.execute("update `proxy_list` set `total_failed` = %d where `id` = %d" \
#                         % (int(ret[random_num]["total_failed"] + 1), int(ret[random_num]["id"]))
#                         )
#                 conn.commit()
#             else:
#                 req.write(str(proxy_ip) + ":" + str(proxy_port) + "<br>")
#                 #req.write(a)
#                 d1 = getdomains(a, ip)
#
#                 b = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n&first=11",10, "http://" + proxy_ip + ":" + str(proxy_port))
#
#                 if b :
#                     for i in getdomains(b, ip):
#                         if i  not in d1:
#                             d1.append(i)
#                         #end if
#                     #end for
#                 #end if
#
#                 c = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n&first=21",10, "http://" + proxy_ip + ":" + str(proxy_port))
#
#                 if c :
#                     for i in getdomains(c, ip):
#                         if i not in d1:
#                             d1.append(i)
#                         #end if
#                     #end for
#                 #end if
#
#                 return d1
#             #end if
#
#             try_times = try_times - 1
#         #end while
#
#         req.write("local<br>")
#
#         a = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n",10, None)
#
#         if a is None:
#             print "error"
#         else:
#             #req.write(a)
#             d1 = getdomains(a, ip)
#
#             b = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n&first=11",10, "http://" + proxy_ip + ":" + str(proxy_port))
#             if b :
#                 for i in getdomains(b, ip):
#                     if i  not in d1:
#                         d1.append(i)
#                     #end if
#                 #end for
#             #end if
#
#             c = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n&first=21",10, "http://" + proxy_ip + ":" + str(proxy_port))
#             if c :
#                 for i in getdomains(c, ip):
#                     if i not in d1:
#                         d1.append(i)
#                     #end if
#                 #end for
#             #end if
#
#             return d1
#         #end if
#
#     except Exception,e:
#         req.write(str(e))
#     #end try
# #end def
#
# # def get_domain_by_ip_proxy(ip, req):
# #     tmp_domains = []
# #     d1= []
# #     try:
# #         conn = MySQLdb.connect(host, user, passwd, db='test', charset='utf8')
# #         cur = conn.cursor(MySQLdb.cursors.DictCursor)
# #
# #         cur.execute("select * from proxy_list")
# #         ret = cur.fetchall()
# #         ret_len = len(ret)
# #
# #         try_times = 3
# #
# #         while try_times > 0:
# #             #break
# #
# #             random_num = random.randint(0, ret_len-1)
# #
# #             proxy_ip   = ret[random_num]["ip"]
# #             proxy_port = ret[random_num]["port"]
# #
# #             cur.execute("update `proxy_list` set `total_used` = %d where `id` = %d" \
# #                         % (int(ret[random_num]["total_used"] + 1), int(ret[random_num]["id"]))
# #                         )
# #             conn.commit()
# #
# #             #req.write("%s:%d" % (proxy_ip,proxy_port))
# #             t1 = time.time()
# #
# #             a = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n",10, "http://" + proxy_ip + ":" + str(proxy_port))
# #             #req.write(a)
# #             t1 = time.time() - t1
# #             if a is None:
# #
# #                 cur.execute("update `proxy_list` set `total_failed` = %d where `id` = %d" \
# #                         % (int(ret[random_num]["total_failed"] + 1), int(ret[random_num]["id"]))
# #                         )
# #                 conn.commit()
# #
# #                 try_times = try_times - 1
# #                 #req.write("<br>error=====<br>")
# #
# #                 continue
# #             else:
# #
# #                 #req.write(a)
# #                 t1_1 = time.time()
# #                 d1 = getdomains(a, ip)
# #                 t1_1 = time.time() - t1_1
# #
# #                 for i in d1:
# #                     tmp_domains.append(i.domain)
# #
# #                     #print "=====1",i.domain,len(i.domain)
# #                 if a.find("下一页") == -1:
# #                     #req.write("t1:%d,t1_1:%d<br>" % (t1, t1_1))
# #                     return d1
# #
# #                 t2 = time.time()
# #                 b = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n&first=11",10,"http://" + proxy_ip + ":" + str(proxy_port))
# #                 t2 = time.time() - t2
# #                 t2_2 = time.time()
# #                 if b :
# #
# #                     for i in getdomains(b, ip):
# #                         #req.write(i.domain)
# #                         if i.domain  not in tmp_domains :
# #                             d1.append(i)
# #                             tmp_domains.append(i.domain)
# #                             #print "=====2",i.domain,len(i.domain)
# #                         #end if
# #                     #end for
# #                     t2_2 = time.time() - t2_2
# #                     if b.find("下一页") == -1:
# #                         #req.write("t2:%d,t2_2:%d<br>" % (t1, t1_1))
# #                         return d1
# #                 #end if
# #
# #
# #                 t3 = time.time()
# #                 c = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n&first=21",10, "http://" + proxy_ip + ":" + str(proxy_port))
# #                 t3 = time.time() - t3
# #                 t3_3 = time.time()
# #                 if c :
# #                     for i in getdomains(c, ip):
# #                         if i.domain not in tmp_domains:
# #                             d1.append(i)
# #                             tmp_domains.append(i.domain)
# #                             #print "=====3",i.domain,len(i.domain)
# #                         #end if
# #                     #end for
# #                 #end if
# #                 t3_3 = time.time() - t3_3
# #
# #                 #req.write("t1:%d,t1_1:%d,t2:%d,t2_2:%d,t3:%d,t3_3:%d<br>" % (t1, t1_1, t2, t2_2, t3, t3_3))
# #                 break
# #
# #             #end if
# #
# #     except Exception,e:
# #         #print e
# #         req.write("get_domain_by_ip_proxy:" + str(e))
# #     #end try
# #
# #     return d1
# # #end def

# def get_domain_by_ip_local(ip, req):
#     tmp_domains = []
#     d1= []
#     try:
#
#         req.write("local,")
#         t1 = time.time()
#         a = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n",10, None)
#
#         t1 = time.time() - t1
#         if a is None:
#             print "error"
#         else:
#
#             #req.write(a)
#             t1_1 = time.time()
#             d1 = getdomains(a, ip)
#             t1_1 = time.time() - t1_1
#
#             for i in d1:
#                 tmp_domains.append(i.domain)
#
#                 #print "=====1",i.domain,len(i.domain)
#             if a.find("下一页") == -1:
#                 req.write("t1:%d,t1_1:%d<br>" % (t1, t1_1))
#                 return d1
#
#             t2 = time.time()
#             b = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n&first=11",10, None)
#             t2 = time.time() - t2
#             t2_2 = time.time()
#             if b :
#
#                 for i in getdomains(b, ip):
#                     #req.write(i.domain)
#                     if i.domain  not in tmp_domains :
#                         d1.append(i)
#                         tmp_domains.append(i.domain)
#                         #print "=====2",i.domain,len(i.domain)
#                     #end if
#                 #end for
#
#             #end if
#
#             t2_2 = time.time() - t2_2
#             if b.find("下一页") == -1:
#                 req.write("t2:%d,t2_2:%d<br>" % (t1, t1_1))
#                 return d1
#             t3 = time.time()
#             c = get_url_content("http://cn.bing.com/search?q=ip%3A%2F**%2F" + ip + "&go=&qs=n&first=21",10, None)
#             t3 = time.time() - t3
#             t3_3 = time.time()
#             if c :
#                 for i in getdomains(c, ip):
#                     if i.domain not in tmp_domains:
#                         d1.append(i)
#                         tmp_domains.append(i.domain)
#                         #print "=====3",i.domain,len(i.domain)
#                     #end if
#                 #end for
#             #end if
#             t3_3 = time.time() - t3_3
#
#             req.write("t1:%d,t1_1:%d,t2:%d,t2_2:%d,t3:%d,t3_3:%d<br>" % (t1, t1_1, t2, t2_2, t3, t3_3))
#             return d1
#         #end if
#
#     except Exception,e:
#         #print e
#         req.write(str(e))
#     #end try
# #end def
"""
domains = get_domain_by_ip("119.75.218.77")

if domains and len(domains) > 0:
    for d in domains:
        print d,get_title_by_url(d)
#print get_title_by_url ("www.163.com")
"""


# def get_proxy_ip_post():
#     conn = MySQLdb.connect(host, user, passwd, db='test', charset='utf8')
#     cur = conn.cursor(MySQLdb.cursors.DictCursor)
#     cur.execute("select * from proxy_list")
#     ret = cur.fetchall()
#     ret_len = len(ret)
#     random_num = random.randint(0, ret_len-1)
#     proxy_ip   = ret[random_num]["ip"]
#     proxy_port = ret[random_num]["port"]
#     proxy_str = "http://"+proxy_ip+":"+str(proxy_port)
#     return proxy_str


# def icp_post_local_ip(url, data):
#     socket.setdefaulttimeout(10)
#     req = urllib2.Request(url)
#     #proxy_support = urllib2.ProxyHandler({'http':proxy_str})
#     cookiefile = "cookiefile"
#     cookieJar = cookielib.MozillaCookieJar(cookiefile)
#     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), urllib2.HTTPHandler);
#     response = opener.open(req)
#     cookieJar.save()
#     req = urllib2.Request('http://tool.chinaz.com/beian.aspx')
#     data = urllib.urlencode(data)
#     #req.write(cookiefile)
#     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), urllib2.HTTPHandler)
#     response = opener.open(req, data)
#     # return response.read()
    
# def icp_post_proxy_ip(url, data,proxy_str):
#     socket.setdefaulttimeout(10)
#     req = urllib2.Request(url)
#     proxy_support = urllib2.ProxyHandler({'http':proxy_str})
#     cookiefile = "cookiefile"
#     cookieJar = cookielib.MozillaCookieJar(cookiefile)
#     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), proxy_support, urllib2.HTTPHandler);
#     response = opener.open(req)
#     cookieJar.save()
#     req = urllib2.Request('http://tool.chinaz.com/beian.aspx')
#     data = urllib.urlencode(data)
#     #req.write(cookiefile)
#     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), proxy_support, urllib2.HTTPHandler)
#     response = opener.open(req, data)
#     # return response.read()
    


# def get_icpinformation_chinaz(domain,req):
#     try:
#         domain = str(domain)
#         #req.write("1.2")
#         urlstr = 'http://tool.chinaz.com/beian.aspx'
#
#
#         """
#         h = httplib2.Http('.domain_cache')
#
#         #req.write(proxy_str)
#         #h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, ip, port))
#
#
#         resp = h.request('http://tool.chinaz.com/beian.aspx?at=img', "GET")
#         cookie =  resp[0]['set-cookie'].split(';')[0]
#         cookie = cookie + ";"
#         headers = {'Cookie': cookie ,'Content-type': 'application/x-www-form-urlencoded'}
#         data="s="+domain+"&code="
#         response,content = h.request(urlstr, 'POST', data, headers=headers)
#         """
#
#         data2 = {'s':domain,'code':''}
#
#         ok_flag = 0
#         times   = 3
#         while ok_flag == 0:
#             try:
#                 proxy_str = get_proxy_ip_post()
#                 content   = icp_post_proxy_ip('http://tool.chinaz.com/beian.aspx?at=img', data2, proxy_str)
#                 ok_flag   = 1
#             except Exception, e:
#                 times = times -1
#                 if times <0:
#                     break
#                 #end if
#             #end try
#         #end while
#
#         if ok_flag == 0:
#             content = icp_post_local_ip('http://tool.chinaz.com/beian.aspx?at=img', data2)
#         #end if
#
#         responsehtml = content
#
#         #print 1.3
#         if (responsehtml.find("查询过于频繁")>0):
#             data = {'code':0}
#             data = json.dumps(data)
#             req.write(data)
#             #req.write('1')
#             return None
#
#         if (responsehtml.find("请输入正确的域名")>0):
#             data = {'code':0}
#             data = json.dumps(data)
#             req.write(data)
#             #req.write('2')
#             return None
#
#
#         soup = BeautifulSoup(responsehtml)
#         table = soup.findAll("table",attrs={'class':'beiantb'})
#
#         if len(table)>0:
#             for aa in table:
#                 aa = str(aa)
#                 soup = BeautifulSoup(aa)
#                 td = soup.findAll("td")
#                 if len(td)==1:
#                     data = {'code':2}
#                     data = json.dumps(data)
#                     req.write(data)
#
#                 else:
#                     company_name = re.findall(r'<tr><td class="tdleft">\xe4\xb8\xbb\xe5\x8a\x9e\xe5\x8d\x95\xe4\xbd\x8d\xe5\x90\x8d\xe7\xa7\xb0</td><td class="tdright">(.*?)</td></tr>',responsehtml)[0]
#                     lic_type = re.findall(r'<tr><td class="tdleft">\xe4\xb8\xbb\xe5\x8a\x9e\xe5\x8d\x95\xe4\xbd\x8d\xe6\x80\xa7\xe8\xb4\xa8</td><td class="tdright">(.*?)</td></tr>',responsehtml)[0]
#                     icp = ""
#                     lic = re.findall(r'<tr><td class="tdleft">\xe7\xbd\x91\xe7\xab\x99\xe5\xa4\x87\xe6\xa1\x88/\xe8\xae\xb8\xe5\x8f\xaf\xe8\xaf\x81\xe5\x8f\xb7</td><td class="tdright">(.*?)</td></tr>',responsehtml)[0]
#                     web_name =  re.findall(r'<tr><td class="tdleft">\xe7\xbd\x91\xe7\xab\x99\xe5\x90\x8d\xe7\xa7\xb0</td><td class="tdright">(.*?)</td></tr>',responsehtml)[0]
#                     url = re.findall(r'<tr><td class="tdleft">\xe7\xbd\x91\xe7\xab\x99\xe9\xa6\x96\xe9\xa1\xb5\xe7\xbd\x91\xe5\x9d\x80</td><td class="tdright">(.*?)</td></tr>',responsehtml)[0]
#                     date = re.findall(r'<tr><td class="tdleft">\xe5\xae\xa1\xe6\xa0\xb8\xe6\x97\xb6\xe9\x97\xb4</td><td class="tdright">(.*?)</td></tr>',responsehtml)[0]
#                     data = {'code':1,
#                             'company_name':company_name,
#                             'lic_type':lic_type,
#                             'icp':icp,
#                             'lic':lic,
#                             'web_name':web_name,
#                             'url':url,
#                             'date':date,
#                             'ok_flag':ok_flag,
#                             'times':times
#                             }
#                     data = json.dumps(data)
#                     req.write(data)
#             return apache.OK
#
#     except Exception,e:
#         data = {'code':0}
#         req.write(e)
#         data = json.dumps(data)
#         req.write(data)
#         return None


"""  
 def get_icpinformation_qycn(domain,req):
    try:
        domain = str(domain)
        urlstr = 'http://tool.qycn.com/icp/'
        h = httplib2.Http('.domain_cache')
        urlstr = urlstr+domain
        response,content  = h.request(urlstr, "GET")
        soup = BeautifulSoup(responsehtml)
        table = soup.findAll("table",attrs={'id':'show_icp_info'})
        if len(table)==1:
            for aa in table:
                aa = str(aa)    
                soup = BeautifulSoup(aa)
                td = soup.findAll("td")
                req.write(len(td))        
    except Exception,e:
        req.write(str(e))
        return 2


"""

'''
def handler(req): 
    
    #req.write(req.args)
    #initLog()
    
    req.content_type="text/html;charset=UTF-8"
    req.no_cache=True
    args_dict = {}
   
    try:
        if req.args and len(req.args) > 0:
            args = req.args.split("&")
            logging.getLogger().error(str(args))
            for a in args:
                if len(a.split("=")) != 2:
                    req.write("error args")
                    return apache.OK
                else:
                    args_dict.setdefault(a.split("=")[0].strip(), a.split("=")[1].strip())
                #end if
            #end for
            
            if args_dict.get("action") and args_dict.get("action") == "cha":
                
                p = re.compile(r'^(?:(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$')
               
                if args_dict.get("ip") and p.match(args_dict.get("ip")) != None:
                    
    
                    domains = get_domain_by_ip_proxy(args_dict.get("ip"), req)
                    #logging.getLogger().debug('domains:' + str(domains))                    
                    if domains and len(domains) > 0:
                        
                        output_str = ""
                        req.write("ok<br>")
                        for d in domains:
                            #print d,get_title_by_url(d)
                            
                            output_str = output_str + d.domain + "#" + d.title + "<br>"
                            
                        #end for
                        #logging.getLogger().error(output_str)
                        req.write(output_str)
                        
                        conn = MySQLdb.connect(host, user, passwd, db='test', charset='utf8')
                        cur = conn.cursor(MySQLdb.cursors.DictCursor)
                        sql = "insert into `result` values(0, '%s', '%s', %d, '%s')" % \
                            (str(req.get_remote_host(apache.REMOTE_NOLOOKUP)), args_dict.get("ip"), len(domains), MySQLdb.escape_string(output_str).decode("utf8"))
                        cur.execute(sql)
                        conn.commit()
                        conn.close()
                    #end if
                #end if
            #end if
            if args_dict.get("action") and args_dict.get("action") == "cha_icp":
                
                get_icpinformation_chinaz(args_dict.get("domain"),req)

                
            #end if   
        else:
            req.write("error args")
        #end if
    except Exception,e:
        req.write(str(e))
    #end try
    
    return apache.OK 
#end def
'''

def ip2int (addr):
    try:
        return struct.unpack("!I",socket.inet_aton(addr))[0]
    except Exception,e:
        return ''  
    #end try
#end def

# def getDomainsByIp(ip,source,req):
#     try:
#         IP_PATTEN = re.compile("^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$")
#         DOMAIN_PATTEN = re.compile("^([0-9a-zA-Z\-\_\.]+)$")
#         if IP_PATTEN.match(ip):
#             list = []
#             ip_int = ip2int(ip)
#             conn = MySQLdb.connect(host, user, passwd, db='waf_hw', charset='utf8')
#             cur = conn.cursor(MySQLdb.cursors.DictCursor)
#             sql = "select * from spider_table_list where cast(ip_start as UNSIGNED) <= %s and cast(ip_end as UNSIGNED) >= %s" % (str(ip_int),str(ip_int))
#             cur.execute(sql)
#             res = cur.fetchone()
#             if res and res['state'] == 1:
#                 table_name = str(res['table_name'])
#                 sql = "select * from `%s` where `ip` = '%s'" % (table_name,ip)
#                 cur.execute(sql)
#                 res = cur.fetchall()
#
#                 for row in res:
#                     domain = row['domain'].strip()
#
#                     if DOMAIN_PATTEN.match(domain) and get_ip_by_host(domain) == ip and domain <> ip:
#                         list.append(domain)
#                     #end if
#                 #end for
#             #end if
#             cur.close()
#             conn.close()
#
#             conn = MySQLdb.connect(host, user, passwd, db='test', charset='utf8')
#             cur = conn.cursor(MySQLdb.cursors.DictCursor)
#             sql = "insert into `search` (`ip`,`source`,`time`) values ('%s','%s',now())" % (ip,source)
#             cur.execute(sql)
#             conn.commit()
#             cur.close()
#             conn.close()
#
#             if len(list) > 0:
#                 return list
#             else:
#                 return None
#             #end if
#         #end if
#
#
#         return None
#     except Exception,e:
#         req.write(str(e))
#         return None
#     #end try
# #end def

def handler(req): 
    
    #req.write(req.args)
    #initLog()
    
    req.content_type="text/html;charset=UTF-8"
    req.no_cache=True
    args_dict = {}
   
    try:
        if req.args and len(req.args) > 0:
            args = req.args.split("&")
            logging.getLogger().error(str(args))
            for a in args:
                if len(a.split("=")) != 2:
                    req.write("error args")
                    return apache.OK
                else:
                    args_dict.setdefault(a.split("=")[0].strip(), a.split("=")[1].strip())
                #end if
            #end for
            
            if args_dict.get("action") and args_dict.get("action") == "cha":
                
                p = re.compile(r'^(?:(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$')
               
                if args_dict.get("ip") and p.match(args_dict.get("ip")) != None:
                    
                    
                    list = []
                    output_str = ""
                    
                    domains = getDomainsByIp(args_dict.get("ip"),str(req.get_remote_host(apache.REMOTE_NOLOOKUP)),req)
                    if domains and len(domains) > 0:
                        for r in domains:
                            if r in list:
                                continue
                            else:
                                list.append(r)
                                output_str += "%s#<br>" % (r)
                            #end if
                        #end for
                    #end if
                    
                    domains = get_domain_by_ip_proxy(args_dict.get("ip"), req)
                    #logging.getLogger().debug('domains:' + str(domains))
                    if domains and len(domains) > 0:
                        pass
                    else:
                        domains = get_domain_by_ip_local(args_dict.get("ip"), req)
                    #end if              
                    if domains and len(domains) > 0:
                        
                        #output_str = ""
                        #req.write("ok<br>")
                        #req.write("len:%s"%len(domains))
                        t = ""
                        for d in domains:
                            #print d,get_title_by_url(d)
                            t = t + d.domain + "#" + d.title + "<br>"
                            if d.domain in list:
                                continue
                            else:
                                list.append(d.domain)
                                output_str = output_str + d.domain + "#" + d.title + "<br>"
                            #end if
                        #end for
                        #logging.getLogger().error(output_str)
                        conn = MySQLdb.connect(host, user, passwd, db='test', charset='utf8')
                        cur = conn.cursor(MySQLdb.cursors.DictCursor)
                        sql = "insert into `result` values(0, '%s', '%s', %d, '%s')" % \
                            (str(req.get_remote_host(apache.REMOTE_NOLOOKUP)), args_dict.get("ip"), len(domains), MySQLdb.escape_string(t).decode("utf8"))
                        cur.execute(sql)
                        conn.commit()
                        conn.close()
                    #end if
                    
                    if output_str != "":
                        output_str = "ok<br>%s" % (output_str)
                        req.write(output_str)
                    #end if
                #end if
            #end if
            if args_dict.get("action") and args_dict.get("action") == "cha_icp":
                
                get_icpinformation_chinaz(args_dict.get("domain"),req)

                
            #end if   
        else:
            req.write("error args")
        #end if
    except Exception,e:
        req.write(str(e))
    #end try
    
    return apache.OK 
#end def

if __name__ == '__main__':
   
    """
    print "======="
    for i in getdomains(tmp, "218.94.157.126"):
        print i.domain,
        print i.title
    
    for i in  get_domain_by_ip_local("218.94.157.126", 1):
        print "============="
        print i.domain,
        print i.title
        print "============="
    """
    
    a = get_url_content("http://cn.bing.com/search?q=ip%3A" + "218.94.157.126" + "&go=&qs=n",10, "http://" + "218.2.51.58" + ":" + str(3128))
    print a
    # get_domain_by_ip_proxy("218.94.157.126", 1)
