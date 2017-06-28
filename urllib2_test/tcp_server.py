#!/usr/bin/evn python
# -*-encoding:UTF8-*-
# Create by zhaozhang@yxlink.com
# On 2017/06/22

import socket
import threading
import logging
import string
import random

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s')

bind_ip = "0.0.0.0"
bind_port = 8000
_random_len = 16
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

logging.DEBUG("[*] Listenin on %s:%d" % (bind_ip,bind_port))

def random_generator():
    field = string.letters + string.digits
    return "".join(random.sample(field, _random_len))

def handle_client(client_socket):
    # 打印出客户端发送的内容
    request = client_socket.recv(1024)

    logging.DEBUG("[*] Received: %s" % request)

    # 返回一个数据包
    client_socket.send("ACK!")
    #client_socket.close()

while True:
    client,addr = server.accept()

    logging.DEBUG("[*] Accepted connection from: %s:%d" % (addr[0],addr[1]))

    # 挂起客户端线程， 处理传入的数据
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()