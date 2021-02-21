#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## ############################################################################
## File Name  # Call EasyOpsCMDB.Python
## Author     # jeremy
## Description  # 提供一个调用优维平台的类
## Requirements #
## Call Syntax  #
## Last Modified# V1.0  2018/02/12  Created
##        V1.1
## ############################################################################


## 数据库里数据无法拼出
## 基于这个接口脚本把数据取出
## date : 20210111
## author : wdll
## 备注 : 运行及其耗时, 持续观察中

import requests
EASYOPS_HOST = "192.168.188.184"
ORG = "1023"
headers = {
  "org": ORG,
  "user": "saadmin",
  "host": "cmdb.easyops-only.com"
}

# 返回所有的业务,是一个列表
def get_business_name():
  business_name = []
  response = requests.get(
    url="http://{0}/business/search".format(EASYOPS_HOST), headers=headers)
  temp = response.json()
  for i in range(len(temp['data'])):
    business=[temp['data'][i]['name'],temp['data'][i]['businessId']]
    business_name.append(business)
  return business_name
  #return temp

# 根据业务ID，列出应用及ID
def get_bussiness_application(businessid):
  applications=[]
  response = requests.get(
    url="http://{0}/business/applist/{1}".format(EASYOPS_HOST,businessid), headers=headers)
  temp = response.json()
  for i in range(len(temp['data'])):
    application_id=(temp['data'][i]['appId'])
    application_name=(temp['data'][i]['name'])
    applications.append([application_name,application_id])
  return applications

# 根据业务ID，列出应用ID
def get_bussiness_appid(businessid):
  application_id = []
  response = requests.get(
    url="http://{0}/business/applist/{1}".format(EASYOPS_HOST,businessid), headers=headers)
  temp = response.json()
  for i in range(len(temp['data'])):
    application_id.append(temp['data'][i]['appId'])
  return application_id

# 通过应用名返回指定的集群信息,返回一个字典
def get_application_ip(application_id):
  response = requests.get(
    url="http://{0}/app/{1}".format(EASYOPS_HOST, application_id), headers=headers)
  temp = response.json()
  cluster_ip = []
  cluster_dict = {}
  # 返回指定的应用列表，肯定只有一个
  for i in range(len(temp['data']['clusters'])):
    # 集群名,做key
    cluster_name = temp['data']['clusters'][i]['name']
    try:
      for j in temp['data']['clusters'][i]['deviceList']:
        try:
          application_memo = temp['data']['memo']
        except Exception as e:
          application_memo = 'null'
        cluster_ip.append([j['ip'], application_memo])  # 各集群下的ip做value
        # 20181230修改 增加备注字段 结束
    except Exception as e:
      cluster_ip.append('null')
    cluster_dict[cluster_name] = cluster_ip
    cluster_name = []
    cluster_ip = []
  return cluster_dict


if __name__ == '__main__':
  all_data = get_business_name()
  for li in all_data:
    this_data = get_bussiness_application(li[-1])
    for i in this_data:
      app_name = i[0] 
      app_id = i[1] 
      #print('%s -- %s' % (app_name, app_id))
      cluster_info = get_application_ip(app_id)
      #print(cluster_info)
      for j in cluster_info: 
        cluster_name = j
        ip_list = cluster_info[cluster_name]
        for ip in ip_list:
          print('%s %s%s' % (ip[0], app_name, cluster_name))
