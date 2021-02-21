#!/bin/bash
cd "$(dirname "$0")"
echo "===============start check===================" >> active_clean.log
echo `date` >> active_clean.log
data_base='../lib/auto-clean.db'
cat /dev/null > nohup.out

cluster_names=`sqlite3 $data_base "select distinct cluster_name from cluster_info;"`
for li in $cluster_names;
do
  t_sql='select distinct type_info from cluster_info where cluster_name like "'$li'"'
  type_infos=`sqlite3 $data_base "$t_sql"`
  cat get_disk_usage_percent.sh > temp-script-active
  for i in $type_infos;
  do
    echo 'disk_useage_percent '$i >> temp-script-active
  done
  t_sql='select distinct ip from app_info where cluster_info like "'$li'"'
  echo $li
  sqlite3 $data_base "$t_sql" > temp-ip.txt
  ./01exec.py -i temp-ip.txt -e temp-script-active >> nohup.out 2>&1
done

need_clean_ip=`cat nohup.out | grep ';;yes;;' | sort -u`
for li in $need_clean_ip;
do
  echo $li >> active_clean.log
  this_ip=`echo $li|awk -F ';;' '{print $3}'`
  this_path=`echo $li|awk -F ';;' '{print $1}'`
  t_sql='SELECT command
  FROM cluster_info
  WHERE
  cluster_name IN
  (select cluster_info from app_info where ip="'$this_ip'")
  and type_info="'$this_path'";'
  sqlite3 $data_base "$t_sql" > temp-script-active
  echo "df -h" >> temp-script-active
  echo '---------'
  cat temp-script-active
  ssh $this_ip -o StrictHostKeyChecking=no -o ConnectTimeout=60 "bash" < temp-script-active
  echo '---------'
done
echo `date` >> active_clean.log
echo "===============check over===================" >> active_clean.log
