import sys
import re

if len(sys.argv) < 2:
    print('argv error!')
    sys.exit()

bv = sys.argv[1]  #得到需要的ＢＶＩ号

def getaddr(bv):
    # pattern1 = r'^%s'%bv
    # f = open('./bvi.txt')   #打开文档
    # while 1:
    #     line = f.readline()
    #     data = re.search(pattern1,line)
    #     if data:
    #         break
    # pattern2 = r'(\d{1,3}\.){3}\d{1,3}/\d{1,3}'
    # while 1:
    #     line = f.readline()
    #     data = re.search(pattern2,line)
    #     if data:
    #         break
    # print(data.group())
    f = open('./bvi.txt', 'rt')
    while 1:
        data = ''
        for line in f:
            if line != '\n':
                data += line
            else:
                break
        if not data:
            break
        pattern1 = r'%s'%bv
        try:
            re_lines = re.match(pattern1,data)
        except:
            continue
        if not re_lines:
            continue
        pattern2 = r'(\d{1,3}\.){3}\d{1,3}/\d{1,3}'
        re_addr = re.search(pattern2,data).group()
        print(re_addr)
        break
if __name__ == '__main__':
    getaddr(bv)