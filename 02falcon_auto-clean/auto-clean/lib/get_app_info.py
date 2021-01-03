#!/usr/bin/python3
import pymysql
import sys
import re
import time
import os

BASE_DIR = sys.path[0]
os.chdir(BASE_DIR)

sql = ("SELECT b.app_ip, a.busniess_name, a.app_name, a.app_cluster, a.app_pgm, a.app_nameid, "
"( CASE "
"WHEN a.app_pgm LIKE %s THEN 'windows' "
"WHEN a.app_pgm LIKE %s THEN 'linux' "
"ELSE 'none' "
"END "
") os "
"from "
"springcmdb.syseasyopspgm a "
"INNER JOIN "
"springcmdb.syseasyops b "
"ON " 
"( a.app_name = b.app_name "
"AND "
"a.app_cluster = b.app_cluster );"
)

conn = pymysql.connect(host='**********', user='cmdb',passwd='********', db='springcmdb', port=3306, charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

cursor.execute(str(sql),('%:\\\\%','%/%'))
result_of_sql = cursor.fetchall()
num1 = len(result_of_sql)
time.sleep(3)

cursor.execute(str(sql),('%:\\\\%','%/%'))
result_of_sql = cursor.fetchall()
num2 = len(result_of_sql)
time.sleep(3)

cursor.execute(str(sql),('%:\\\\%','%/%'))
result_of_sql = cursor.fetchall()
num3 = len(result_of_sql)

f = open("app_info.txt", "w", encoding="utf-8")


if num1 == num2 and num2 == num3:
  result1 = "ok " + str(num1)
  print(result1)
  for li in result_of_sql :
    if str(li['os']) != 'windows' :
      this_str = str(li['app_ip'])
      this_str = this_str + " " + str(li['app_name'])
      this_str = this_str + str(li['app_cluster']) + "\n"
      f.write(str(this_str))
else:
  result1 = "fail null " 
  print(result1)

cursor.close()
conn.close()
f.close()
