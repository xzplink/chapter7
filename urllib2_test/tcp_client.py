#!/usr/bin/env python
#-*-encoding:UTF8-*-

import socket
import time

target_host = "192.168.98.138"
target_port = 8000

# 建立一个sokcet对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接客户端
client.connect((target_host,target_port))
while True:
    time.sleep(180)
    # 发送一些数据
    client.send("GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n")
    # 接收一些数据
    response = client.recv(4096)
    print response
    time.sleep(1)