#!/usr/bin/python3
# date : 2020-11-28
# v4 : 修改ip空格不然无法使用
# v5 : 修改中文读取乱码
# 使用 : --help 查看
import os, shutil, argparse, sys, time, threading
import subprocess


# 定义变量IP_FILE, TMP_FILE
def pre_fun():
    # 生成tmp临时目录
    #BASE_DIR = os.getcwd()
    BASE_DIR = sys.path[0]
    os.chdir(BASE_DIR)
    if not os.path.isdir('tmp'):
        os.makedirs('tmp')
    # 定义临时目录, 临时ip文件, 临时执行文件
    TMP_DIR = os.path.join(BASE_DIR, 'tmp')
    IP_FILE = os.path.join(TMP_DIR, 'ip.txt')
    TMP_FILE = os.path.join(TMP_DIR, 'tmp-exec-file')
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip_file", help="ip文件", type=str, default=IP_FILE)
    parser.add_argument("-ip", "--ip", help="ip", type=str, default=IP_FILE)
    parser.add_argument("-e", "--exec_file", help="执行文件", type=str, default=TMP_FILE)
    parser.add_argument("-c", "--command", help="执行文件", type=str, default=TMP_FILE)
    args = parser.parse_args()
    exec_file = args.exec_file
    exec_command = args.command
    gen_ip_fun(args.ip, args.ip_file, IP_FILE)
    gen_exec_fun(exec_file, exec_command, TMP_FILE)
    return IP_FILE, TMP_FILE


# 通过参数-i或ip; 生成ip文件
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


# 通过参数-e或-c; 生成执行文件
def gen_exec_fun(exec_file, exec_command, TMP_FILE):
    if str(exec_file) != str(TMP_FILE) and str(exec_command) != str(TMP_FILE):
        print("不能同时指定-c和-e参数")
        sys.exit()
    elif str(exec_file) != str(TMP_FILE):
        source = str(exec_file)
        target = TMP_FILE
        shutil.copy(source, target) 
    elif str(exec_command) != str(TMP_FILE):
        f = open(TMP_FILE, "w")
        f.write(str(exec_command))
        f.close()


# 读取配置文件 IP_FILE, TMP_FILE, 执行
def run(IP_FILE, TMP_FILE):
    ip_lists = []
    #ip_file = open(IP_FILE, 'rb')
    ip_file = open(IP_FILE, 'r', encoding="utf-8")
    machines_info = []

    for li in ip_file :
        if li and '#' not in str(li):
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
                if ip in str(li_m) :
                    this_info = str(li_m)
            t_ip = str(ip).split( ' ' )
            t_ip = t_ip[0]
            t_exec_file = str(TMP_FILE)
            t_name = myThread(t_exec_file, t_ip, this_info)
            this_threads.append(t_name)
        [ thr.start() for thr in this_threads ]
        [ thr.join() for thr in this_threads ]
        print('-----------------------------------------')


class myThread (threading.Thread):
    def __init__(self, exec_file, tip, tinfo):
        threading.Thread.__init__(self)
        self.exec_file = exec_file
        self.tip = tip
        self.tinfo = tinfo
    def run(self):
        this_ip = str(self.tip)
        this_str="start :" + str(this_ip)
        print (this_str)
        try :
            command = "scp -o ConnectTimeout=5 -q -r " + str(self.exec_file)  + " root@" +  str(this_ip) + ":/home"
            res = subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=9)
        except Exception as e:
            error_info = "===> :" + str(self.tinfo) + "\nerror info: " + str(e) + "\n\n"
            print(error_info)
        else :
            res = os.popen(('ssh root@%s  -o ConnectTimeout=5 "cd /home;chmod +x tmp-exec-file && ./tmp-exec-file;rm -f tmp-exec-file"') % (str(this_ip))).read()
            this_str = "===> :" + self.tinfo + "\n" + str(res) + "\n\n"
            print (this_str)
 
if __name__ == '__main__':
    IP_FILE, TMP_FILE = pre_fun()
    run(IP_FILE, TMP_FILE)
