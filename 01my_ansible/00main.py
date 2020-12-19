#!/usr/bin/python3
# date : 2020-09-24
# v1 : control mode
# info : 未完成
import os, shutil, argparse, sys, time, threading
import subprocess


def pre_fun():
    #BASE_DIR = os.getcwd()
    BASE_DIR = sys.path[0]
    os.chdir(BASE_DIR)
    TMP_DIR = os.path.join(BASE_DIR, 'tmp')
    IP_FILE = os.path.join(TMP_DIR, 'ip.txt')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip_file", help="ip文件", type=str, default=IP_FILE)
    parser.add_argument("-ip", "--ip", help="ip", type=str, default=IP_FILE)
    parser.add_argument("-f", "--file", help="剧本文件", type=str)
    args = parser.parse_args()
    gen_ip_fun(args.ip, args.ip_file, IP_FILE)
    gen_pb_fun(args.file)

def gen_ip_fun(args_ip, args_ip_file, IP_FILE):
    if args_ip != IP_FILE and args_ip_file != IP_FILE:
        print("不能同时指定-i和-ip参数")
        sys.exit()
    elif args_ip != IP_FILE:
        f = open(IP_FILE, "w")
        f.write(args_ip)
        f.close()
    elif args_ip_file != IP_FILE:
        if os.path.isfile(args_ip_file):
            shutil.copy(args_ip_file, IP_FILE)
        else:
            print('ip file not exists!')
            sys.exit()

def gen_pb_fun(paly_book):


if __name__ == '__main__':
    pre_fun()
    this_file = open(this_file, 'rb')
    for li in this_file:
        if '#' in str(li) and 'step' in str(li):
            this_info = str(li).split('\'')
            this_info = str(this_info[1]).split('\\')
            this_info = str(this_info[0])
            print(str(this_info))
        else:
            way = str(li).split('\'')
            way = str(way[1]).split('\\')
            way = str(way[0])
            this_command = way_fun(way)
            if this_command != "None":
                this_command = os.path.join(TOOLS_DIR, this_command)
            print(this_command)
    this_file.close()
