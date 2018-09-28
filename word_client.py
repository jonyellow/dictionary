from socket import *
import sys
import os
from time import sleep
import getpass  #隐藏显示输入时的密码

if len(sys.argv) < 3:
    pring('argv error!')
    os._exit()
port = int(sys.argv[2])
ADDR = (sys.argv[1], port)

#创建功能函数
def do_1(s):
    print('++++欢迎注册：＝＝＝＝＝＝＝＝＝＝')
    while 1:
        name = input('name:')
        password = getpass.getpass()
        info = 'N ' + name + ' ' + password
        s.send(info.encode())
        sleep(0.1)
        data = s.recv(1024)
        if data == b'name exists':
            print('用户已存在！请重新输入！')
            continue
        elif data == b'good':
            print('注册成功！')
            wordSelect(s,name)

def do_2(s):
    print('++++++登录：===============')
    while 1:
        name = input('name:')
        password = getpass.getpass()
        info = 'D ' + name + ' ' + password
        s.send(info.encode())
        sleep(0.1)
        data = s.recv(1024)
        if data == b'nameerror':
            print('用户名不存在！请重新输入！')
            continue
        elif data == b'passworderror':
            print('密码错误！请重新输入！')
        elif data == b'good':
            print('登录成功！')
            wordSelect(s,name)
#退出
def do_3(s):
    s.close()
    print('客户端退出！')
    os._exit(0)
#创建查询函数
def wordSelect(s,name):
    while 1:
        print('''+++++nice process==================
            1)查单词　　　2)查个人历史记录
            ====================================
            ''')
        data = input('commond:')
        if data not in '12':
            print('请输入１　２中的一个！')
            continue
        else:
            if data == '1':
                data = input('word:')
                if data == '##':
                    print('客户端退出！')
                    os._exit(0)
                wordinput = 'M ' + data + ' ' + name
                s.send(wordinput.encode())
                data = s.recv(4096)
                if data == b'worderror':
                    print('没有该单词！')
                else:
                    print(data.decode())
            elif data == '2':
                wordinput = 'M ' + 'H ' + name
                s.send(wordinput.encode())
                data = s.recv(1024).decode()
                if data == b'noist':
                    print('没有历史记录！')
                else:
                    print(data)

def main():
    #创建网络连接
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect(ADDR)
    except:
        print('连接服务器失败！')
        sys.exit('客户端退出！')
    while 1:
        print('''+++++nice process==================
            1)注册　　　2)登录　　　３）退出
            ====================================
            ''')
        sys.stdin.flush() #清除标准输入
        data = input('input:')
        if data not in "123":
            print('请输入１　２　３　中的一个！')
            continue
        elif data == '1':
            do_1(s)
        elif data == '2':
            do_2(s)
        elif data == '3':
            do_3(s)

if __name__ == "__main__":
    main()
