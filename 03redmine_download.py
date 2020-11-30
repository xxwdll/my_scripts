#!/usr/bin/python3
import sys, io, re, os, zipfile
from urllib import request


def get_download_url(sub_url, redmine_type):
  url_key_pattern = re.compile(r"href=\".*\"")
  url_key = url_key_pattern.findall(str(sub_url))
  url_key_pattern = re.compile(r"\/redmine.*\"")
  url_key = url_key_pattern.findall(str(url_key))
  sub_url = str(url_key[0])
  sub_url = sub_url.split('"')
  sub_url = str(sub_url[0])
  if redmine_type == '01' :
    download_url = "http://redmine.springgroup.cn" + sub_url
  elif redmine_type == '02' :
    download_url = "http://redmine02.springgroup.cn" + sub_url
  return download_url

def get_file_name(sub_url):
  url_key_pattern = re.compile(r"href=\".*")
  url_key = url_key_pattern.findall(str(sub_url))
  this_file_name = str(url_key[0])
  this_key_pattern = re.compile(r"\>.*?\<")
  this_file_name = this_key_pattern.findall(str(this_file_name))
  this_file_name = str(this_file_name[0])
  this_file_name = this_file_name.strip('>,<')
  return this_file_name


def pre_fun(save_dir, redmine_number):
  len_redmine_number = len(redmine_number)
  if len_redmine_number == 6:
    #浏览器登录后得到的cookie
    cookie_str = r'_redmine_session=ajhuOC9xbG9NaWlyUjJ4RTBzcDF4cjl1SVVzUlF4V1dURitCQ2x1U0FpQ1kva1ZrM1ppZ3FDTjVXbnNkdlNHSld3WCt4UjVIYlFBcFhMd29mTVdTc290ZGk5WGRERzl0RmR6V3VubFMxQkF1VGQvQlVGcHdEZWhkMTJFMzNGbVdQSlhYcnJldG81aGxUMGMxK0k0TWxLV1FJdHNnakx5Zm8yNWFMdXk4NWpYZVpGQmVBeFc1eUVDQWJFUGlwNjV4SXB1S0IxKy9EYUVOczNJMUU4VnEyMzh3eDRLYW9JRWVKL2toZVNhTnkvN051RFVVVnExYlU2Zmk5U2xPUkFzc0tqdWl2eDFJMFBOeFJoUmE1dklGaVNsQm1NNi8xazRLcG1icHRFS01DUTR4MGt3dENnYWs4TFB6WENZemZZQW45MU1qNlBTWmcxTytXbHZhWkZPck9pdXZVMzZpWVl6VlBHUmtHMjVTQkNTWS9TRWtjbFhRdGJGaWVHazVseDFSMHJ5WGd3dDBTTGNNK3plV3VaZWI0NVcxVmZBeWR6N3ZkUnQ4UWN6ZStIRHdCUi9tVm5GR044dEMvQW14czR3TFpKMHZEWDFSYlhqbXN4dzlYZWY0S1ZxZVpBRE5Vc2ZaSmlzdFFkZ0xuQ0FhZi9DMExtTkR0T0dSY2VIRHl2L0hqcjVYME02S3E5blBHeGdYVkh2LzhyeW5iRmxiRHJJTW05UG56MTIzSGpZPS0tK2tCc0cway9MNHZTdzQ0Ynd5K21YQT09--0d7676e2c2d3bad6d03b6fce8bb19986b06a3be0'
    #登录后才能访问的网页
    redmine_url = 'http://redmine.springgroup.cn/redmine/issues/' + redmine_number
    redmine_type = '01'
  elif len_redmine_number == 4:
    cookie_str = r'_redmine_session=Yk9lZEcvUG5KYVNDMXAvMGs3MG5McExRbFBSdmc5ZUl0ZEVXKzJSUi93Y2lYSlV6bDhndGpVMlB3UGxHOWdlK3pqaFV3TTBjREFvOEVQWHUraklsbHU0TUcvdmRsVE9aUTZtSFdIVWV3c1diY0VucUZWQnhTNTdyZXI0TzM3WWtobWF2dnp0VUFUNWQ4bCtCQTN1VXFEMENlY1VmRWZuQk9na3l6TFRXcDd3eU9TY3psZVZsanIveGpaT3ZaeDlXS1R4eUFtRGtaWEltQmFqOTZLR1JhUjZhWUFNWXJvbkhTYlJnMmpTOGxUR0VXUGJTYWRGNjhDU0F5TGJDZjlMUUl5ZnNmRnNPcDg1OWF5d2h0QU8rVFVBdmd5SkphYjhDRGJYS3hDNGg3cGxLOGllSERXam5lWVZvVHBWMFdEUXlZbUx6d1pxRjN1SEttT0kwR0VqSXdVWlZYSGxNaUxneUFpNTNMOVRzVDlIeFY4cVhEUXVPZGhuNWRRY1BzakFiYzM1UVJFWnpLODQ1ZmsxYndnUmFkWW1CVDg0VHlRcDF4U3hOYm5lanUyV3J0elNuRTdHczh6VEZ2ZC9yM3VkYnBKc0czRXo2Vk9QUW9rRUhVWS9WcnVLdEFIeSs4dldOdzBYcE9HSDZqZjkvOVRpS2hQeHhvazBPVTdzYzFsaWVNcUVtR1J2eHpRa1BqNStPa3ZWcmZLUFZBT05seUxsR1hPV0RsMzRnb2FWSmwwbG1pT1hVOGNpRGVSWE8vQ01zbUNSamtOcjRZcmN5eHQvajUzYXpoelg1T2psd2RBd0VNalU2WlV5TWhScz0tLWRVc2swV1FpRGlEdGZ5SVZLeEtHemc9PQ%3D%3D--8c8f689ced7f53990688848cb0ea665f0d1a011b'
    #登录后才能访问的网页
    redmine_url = 'http://redmine02.springgroup.cn/redmine/issues/' + redmine_number
    redmine_type = '02'
  else:
    print('redmine号 可能有误')
    sys.exit()
  os.chdir(save_dir)
  redmine_number_file = redmine_number + '.zip'
  if not os.path.isdir(redmine_number):
    os.makedirs(redmine_number)
  if os.path.isfile(redmine_number_file):
    os.remove(redmine_number_file)
  os.chdir(redmine_number)
  file_list = os.listdir()
  for li in file_list:
    os.remove(li)
  

  return redmine_url, cookie_str, redmine_type


def start_download(redmine_url, cookie_str, redmine_type):
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
  req = request.Request(redmine_url)
  #设置cookie
  req.add_header('cookie', cookie_str)
  #设置请求头
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
  resp = request.urlopen(req)
  #print(resp.read().decode('utf-8'))
  #this_text = resp.read().decode('utf-8')
  while resp:
    li = resp.readline().decode('utf-8')
    if "</html>" in li:
      break
    # 匹配文件名 和 下载 url
    if ("rar" in li or "zip" in li or "tgz" in li or "tar" in li or "配置" in li or "更新操作手册.html" in li)\
    and ("数据库" not in li and "已添加" not in li)\
    and ("href" in li and "download" in li):
      # 文件名
      file_name = get_file_name(li)
      # 下载链接 
      download_url = get_download_url(li, redmine_type)
      print("--- %s ---" % (file_name))
      req1 = request.Request(download_url)
      #设置cookie
      req1.add_header('cookie', cookie_str)
      #设置请求头
      req1.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
      
      this_file = request.urlopen(req1)
      data = this_file.read()
      with open(file_name.encode('utf-8'), "wb") as code:
        code.write(data)


if __name__ == '__main__':

  #读取第一个参数, redmine号码
  #redmine_number = sys.argv[1]
  redmine_number = input("输入redmine号码==> ")
  #下载存放路径
  #save_dir = "/home/xxwdll/soft/nginx/download/tmp"
  save_dir = os.getcwd()
  redmine_url, cookie_str, redmine_type = pre_fun(save_dir, redmine_number)
  #开始下载
  start_download(redmine_url, cookie_str, redmine_type)
