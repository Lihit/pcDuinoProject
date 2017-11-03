# -*- coding:utf-8 -*-
'''
author:wenshao
time:2017-11-3
'''
from socket import *
import json


def main():
    try:
        udpSocket = socket(AF_INET, SOCK_DGRAM)
        bindAddr = ('', 8899)
        udpSocket.bind(bindAddr)
        while True:
            print('---------等待新的数据来----------')
            json_recv, addr = udpSocket.recvfrom(2048)
            json_string=json_recv.decode('utf-8')
            if len(json_string)>0:
                recv_list = json.loads(json_string)
                with open('myfile.txt', 'a') as fp:
                    for i in recv_list:
                        fp.write(','.join(i) + '\n')
            else:
                break
    except Exception as e:
        print(e)
    finally:
        print('----------程序结束----------')
        udpSocket.close()


if __name__ == '__main__':
    main()
