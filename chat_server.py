"""
chat room
env:python3.6
socket udp & fork exc
"""

from socket import *
import os, sys

# 全局变量：很多封装模块都要用或者有特定含义的变量
HOST = '0.0.0.0'
POST = 4396
ADDR = (HOST, POST)

# 存储用户 {name:address}
user = {}


# 退出聊天
def do_quit(s, name):
    msg = "\n%s 退出了群聊" % name
    for i in user:
        if i == name:
            s.sendto(b'EXIT', user[i])
        else:
            s.sendto(msg.encode(), user[i])
    del user[name]  # 删除用户


# 处理聊天
def do_chat(s, name, text):
    msg = "\n%s: %s" % (name, text)
    for i in user:
        # 不发送自己
        if i != name:
            s.sendto(msg.encode(), user[i])


# 处理用户登录
def do_login(s, name, addr):
    if name in user or '管理员' in name:
        s.sendto("\n用户名已存在".encode(), addr)
        return
    else:
        s.sendto(b'OK', addr)  # 可以进入
    # 通知其他人
    msg = "\n欢迎 %s 加入群聊" % name
    for i in user:
        s.sendto(msg.encode(), user[i])
    user[name] = addr  # 加入字典


# 循环获取客户端请求
def do_request(s):
    while True:
        data, addr = s.recvfrom(1024)
        tmp = data.decode().split(' ', 2)
        # 根据不同的请求类型 执行不同的事件
        if tmp[0] == 'L':  # 登录
            do_login(s, tmp[1], addr)
        elif tmp[0] == 'C':  # 聊天
            do_chat(s, tmp[1], tmp[2])
        elif tmp[0] == 'Q':  # 退出
            do_quit(s, tmp[1])


# 搭建网络
def main():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)
    pid = os.fork()
    if pid == 0:
        # 管理员消息处理
        while True:
            msg = input("管理员消息：")
            msg = "C 管理员 "+ msg
            s.sendto(msg.encode(),ADDR)
    else:
        do_request(s)  # 接收客户端请求


if __name__ == '__main__':
    main()
