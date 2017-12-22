# -*- coding:utf-8 -*-
'''
author:wenshao
time:2017-11-3
'''
from socket import *
import json
import datetime
import os


def main():
    try:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        if not os.path.exists(time_str):
            os.mkdir(time_str)
        udpSocket = socket(AF_INET, SOCK_DGRAM)
        bindAddr = ('', 8899)
        udpSocket.bind(bindAddr)
        while True:
            print('---------等待新的数据来----------')
            json_recv, addr = udpSocket.recvfrom(2048)
            json_string = json_recv.decode('utf-8')
            print('---------接收到新的数据----------')
            print(json_string)
            if len(json_string) > 0:
                recv_list = json.loads(json_string)
                for i in recv_list:
                    if i[0] == 0:
                        with open(os.path.join(time_str, 'InputFace.txt'), 'a') as fp:
                            i_new = i[1:]
                            fp.write(','.join(i_new) + '\n')
                    else:
                        with open(os.path.join(time_str, 'RecoFace.txt'), 'a') as fp:
                            i_new = i[1:]
                            fp.write(','.join(i_new) + '\n')
            else:
                break
    except Exception as e:
        print(e)
    finally:
        print('----------程序结束----------')
        udpSocket.close()


if __name__ == '__main__':
    main()
