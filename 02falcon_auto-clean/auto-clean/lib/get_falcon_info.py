#!/usr/bin/python3
import pymysql, sys, os, datetime

def getTodayAndYesterday(): 
  today=datetime.date.today() 
  oneday=datetime.timedelta(days=1) 
  yesterday=today-oneday  
  today='%'+str(today)+'%'
  yesterday='%'+str(yesterday)+'%'
  return today, yesterday

BASE_DIR = sys.path[0]
os.chdir(BASE_DIR)

this_today, this_yesterday = getTodayAndYesterday()

sql = ("select endpoint, metric, priority, note, timestamp "
"from event_cases "
"where "
"status = 'PROBLEM' "
"and "
"(timestamp like '%s' or timestamp like '%s')"
"order by timestamp desc limit 100;"
)

conn = pymysql.connect(host='*********', user='root',passwd='*********', db='alarms', port=3306, charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

cursor.execute(sql % (this_today, this_yesterday))
result_of_sql = cursor.fetchall()

for li in result_of_sql :
  this_str = str(li['endpoint'])
  this_str = this_str + " " + str(li['metric'])
  this_str = this_str + " " + str(li['priority'])
  this_str = this_str + " " + str(li['note']) 
  #this_str = this_str + " " + str(li['timestamp']) 
  print(this_str)

cursor.close()
