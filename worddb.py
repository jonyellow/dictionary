#!/usr/bin/python3

#该模块用于将txt文件导入数据库表中

import pymysql
import re
#打开文件
f = open('./word.txt','r')
def txtToMysql():
    #创建数据库对象
    db = pymysql.connect('localhost', 'root', '123456', 'worddb')

    #创建数据库游标对象
    cur = db.cursor()

    #用游标对象操作
    for line in f:    #插入数据到数据库表中
        # wd = re.match(r'\S+', line).group()
        # exp = re.findall(r'\w+\s+(.*)', line)[0]
        linelist = line.split(re.search(r'\s+',line).group())
        inserttable = "insert into worddict (word,ex) values ('%s','%s');"%(linelist[0], linelist[1])
        try:
            cur.execute(inserttable)
    #提交操作到数据库
            db.commit()
        except:
            db.rollback()
    #关闭游标对象
    cur.close()
    #关闭数据库连接
    db.close()
    #关闭文件
    f.close()
if __name__ == "__main__":
    txtToMysql()