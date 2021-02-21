#!/bin/bash
# author : wdll
# date   : 2021013
# info   : 从falcon中获取最新报警数据,执行本地预存脚本
# v3     : 增加alarm-error.log 日志, 便于添加修改信息
# v4     : 修改useless判断次数,减少误判
# v5     : 修改日期格式
cd "$(dirname "$0")"
this_time=`date '+%Y-%m-%d_%H-%M-%S'`
time_tag=`date '+%Y-%m-%d_%H'`
#./alarm-get-falcon.sh | grep df.bytes | grep mount=/ > temp-ip.txt
./get_falcon_info.py | grep df.bytes | grep mount=/ > temp-ip.txt
# 过滤出磁盘报警信息 处理
cat temp-ip.txt | sort -u | while read li;
do
  this_ip=`echo $li | awk '{print $1}' | awk -F '-' '{print $NF}'`
  this_path=`echo $li | grep df.bytes | grep mount=/ | awk '{print $2}' | awk -F ',' '{print $2}' | awk -F '=' '{print $2}'`
  this_sql='SELECT command
  FROM cluster_info
  WHERE
  cluster_name IN
  (select cluster_info from app_info where ip="'$this_ip'")
  and type_info="'$this_path'";'
  sqlite3 auto-clean.db "$this_sql" > temp-script
  this_commad=`cat temp-script`
  if [[ ! -z "$this_commad" ]];then
    existence_of_exec_info=`cat ../log/alarm-clean.log | grep -A3 'ip==>' | tail -30 | grep -a2 $time_tag | grep -A1 -w $this_ip | grep $this_path | wc -l`
    if [[ -z "$existence_of_exec_info" ]] || [[ "$existence_of_exec_info" -le "2" ]];then
      echo "ip==> " $this_ip
      echo "path==> " $this_path
      echo "time==> " $this_time
      echo "df -h" >> temp-script
      echo '---------'
      cat temp-script
      ssh $this_ip -o StrictHostKeyChecking=no -o ConnectTimeout=60 "bash" < temp-script
      echo '---------'
    else
      #echo '---USELESS---' >> ../log/alarm-error.log
      echo "---USELESS---" `date` "==>" $this_ip "--" $this_path >> ../log/alarm-error.log
    fi
  else
    existence_of_null_info=`cat ../log/alarm-clean.log | grep -A3 'ip==>' | tail -30 | grep -a2 $time_tag | grep -A1 -w $this_ip | grep $this_path | wc -l`
    if [[ -z "$existence_of_null_info" ]] || [[ "$existence_of_null_info" -le "3" ]];then
      echo "ip==> " $this_ip
      echo "path==> " $this_path
      echo "time==> " $this_time
      echo '-----null-----'
      echo "root_dir="$this_path > temp-script
      cat temp-script_null >> temp-script
      #cat temp-script
      ssh $this_ip -o StrictHostKeyChecking=no -o ConnectTimeout=60 "bash" < temp-script
      file_info=`tail -10 ../log/alarm-clean.log | grep 'clean file==>'`
      echo "---NULL AUTOADDED---" `date` "==>" $this_ip "--" $this_path >> ../log/alarm-error.log
      echo $file_info >> ../log/alarm-error.log
      echo '---------'
    else
      #echo '---NULL---' >> ../log/alarm-error.log
      echo "---NULL---" `date` "==>" $this_ip "--" $this_path >> ../log/alarm-error.log
    fi
  fi
done
