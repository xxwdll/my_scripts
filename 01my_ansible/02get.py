#!/usr/bin/python3
# -*- coding:utf-8 -*-
# date : 2020-10-28
# v3 : 修改ip空格不然无法使用
# v4 : 修改中文读取乱码
import os, shutil, argparse, sys, time, threading
import subprocess


def pre_fun():
    #BASE_DIR = os.getcwd()
    BASE_DIR = sys.path[0]
    os.chdir(BASE_DIR)
    if not os.path.isdir('tmp'):
        os.makedirs('tmp')
    TMP_DIR = os.path.join(BASE_DIR, 'tmp')
    IP_FILE = os.path.join(TMP_DIR, 'ip.txt')
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help="远程服务器上的文件路径", type=str, default="None")
    parser.add_argument("-t", "--target", help="存到本地路径", type=str, default="None")
    parser.add_argument("-i", "--ip_file", help="ip文件", type=str, default=IP_FILE)
    parser.add_argument("-ip", "--ip", help="ip", type=str, default=IP_FILE)
    args = parser.parse_args()
    target_file = str(args.source)
    save_dir = str(args.target)
    if target_file == "None" or save_dir == "None":
        print("-s参数, -t参数必须指定")
        sys.exit()
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    gen_ip_fun(args.ip, args.ip_file, IP_FILE)
    return IP_FILE, target_file, save_dir


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


def run(IP_FILE, target_file, save_dir):
    ip_lists = []
    machines_info = []
    #ip_file = open(IP_FILE, 'rb')
    ip_file = open(IP_FILE, 'r', encoding="utf-8")
    for li in ip_file :
        if li and '#' not in str(li) :
            machines_info.append(str(li))
            li = str(li).split()
            li = li[0]
            ip_lists.append(str(li))
    ip_file.close()

    #max_tasks = input('请输入并行个数:')
    max_tasks = 10
    while ip_lists :
        this_ip_lists = []
        for li in range(max_tasks) :
          if ip_lists :
            this_ip = ip_lists.pop(0)
            this_ip_lists.append(str(this_ip))
        this_threads = []
        for ip in this_ip_lists :
            for li_m in machines_info :
                if ip in li_m :
                    this_info = str(li_m)
            ip = str(ip).split(' ')
            ip = str(ip[0])
            this_save_dir = os.path.join(save_dir, str(ip))
            if not os.path.isdir(this_save_dir):
                os.makedirs(this_save_dir)
            t_name = str(ip)
            t_name = myThread(this_info, t_name, target_file, this_save_dir)
            this_threads.append(t_name)
    [ thr.start() for thr in this_threads ]
    [ thr.join() for thr in this_threads ]
    print('-----------------------------------------')


class myThread (threading.Thread):
    def __init__(self, this_info, name, target_file, save_dir):
        threading.Thread.__init__(self)
        self.this_info = this_info
        self.name = name
        self.target_file = target_file
        self.save_dir = save_dir
    def run(self):
        this_str="start :" + self.this_info
        print (this_str)
        try :
            os.system(('scp -o ConnectTimeout=5 -q -r root@%s:%s %s') % (str(self.name), str(self.target_file), str(self.save_dir)))
        except :
            this_str = "==> " + self.this_info + '\n' + "connect fail !'" + '\n\n'
            print (this_str)
        else :
            this_save_dir=str(self.save_dir)+'/'+str(self.name)
            res = os.popen(('cd %s && ls -l') % (str(self.save_dir))).read()
            this_str = "==> " + self.this_info + '\n' + str(res) + '\n\n'
            print (this_str)


if __name__ == '__main__':
    IP_FILE, target_file, save_dir = pre_fun()
    run(IP_FILE, target_file, save_dir)  
