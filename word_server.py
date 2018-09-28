'''
name: jon yellow
phone: 123456
project: word select server
'''

from socket import *
from time import sleep
import pymysql
import signal
import sys
import os


#创建子进程函数
def wordSelect(conn, db, addr):
    #创建数据库游标对象
    cur = db.cursor()
    #接受消息
    while 1:
        commond = conn.recv(1024).decode()
        if not commond:
            cur.close() #关闭数据库游标
            conn.close()
            print(addr)
            sys.exit('客户端退出！') #子进程退出
        com = commond.rstrip('\n').split(' ')

        #进行第一条指令判断
        if com[0] == 'N':#注册
            #判断用户名是否存在
            sql = "select username,password from userinfo where username='%s'"%com[1]
            try:
                cur.execute(sql)
                db.commit()
            except:
                db.rollback()
            rows = cur.fetchone()
            if not rows:
                insert = "insert into userinfo (username,password) values ('%s','%s')"%(com[1],com[2])
                try:
                    cur.execute(insert)
                    db.commit()
                except:
                    db.rollback()
                conn.send(b'good')
            else:
                conn.send(b'name exists')

        elif com[0] == 'M':#查单词
            if com[1] == 'H':
                sql = "select word,time from hist where name='%s'"%com[2]
                try:
                    cur.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                rows = cur.fetchall()
                if not rows:
                    conn.send(b'nohist')
                else:
                    row = ''
                    for i in range(len(rows)):
                        row += rows[i][0] +' ' + str(rows[i][1]) + ' '
                    conn.send(row.encode())
            else:
        #进行单词查询，并写入hist表中
                sql = "select word,ex from worddict where word='%s'"%com[1]
                try:
                    cur.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                rows = cur.fetchone()
                if not rows:
                    conn.send(b'worderror')
                else:
                    insert = "insert into hist (name,word) values ('%s','%s')"%(com[2],com[1])
                    try:
                        cur.execute(insert)
                        db.commit()
                    except:
                        db.rollback()
                    info = rows[0] + ':' + rows[1]
                    conn.send(info.encode())
        elif com[0] == 'D':#登录
            sql = "select username,password from userinfo where username='%s'"%com[1]
            try:
                cur.execute(sql)
                db.commit()
            except:
                db.rollback()
            rows = cur.fetchone()
            #判断用户名是否存在，存在密码是否正确
            if not rows:
                conn.send(b'nameerror')
            else:
                if com[2] == rows[1]:
                    conn.send(b'good')
                else:
                    conn.send(b'passworderror')




#创建主进程
def main():
    #创建数据库连接
    db = pymysql.connect('localhost', 'root','123456', 'worddb')

    #忽略子程序退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    
    #创建套接字
    s = socket(AF_INET, SOCK_STREAM)
    #设置端口立即释放
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #绑定服务端地址
    s.bind(('',8888))
    s.listen(5)
    #创建连接套接字
    print('waitting for connect...')
    while 1:
        try:
            conn, addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出！')
        except Exception as e:
            print("服务器异常:",e)
            continue
        print(addr, '已连接服务器！')
        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            wordSelect(conn, db, addr)
        else:
            conn.close()
            continue
if __name__ == '__main__':
    main()