#!/bin/bash

alarmmain_pid=`ps -ef | grep alarm-main.sh | grep -v grep | awk '{print $2}'`
clean_disk_pid=`ps -ef | grep falcon-clean-disk.sh | grep -v grep | awk '{print $2}'`

stop_clean_disk_pid(){
  while true;
  do
    echo '正在执行清理操作,请稍后..'
    clean_disk_pid=$(ps -ef | grep falcon-clean-disk.sh | grep -v grep | awk '{print $2}')
    if [[ -z "$clean_disk_pid" ]];then
      alarmmain_pid=`ps -ef | grep alarm-main.sh | grep -v grep | awk '{print $2}'`
      kill -9 $alarmmain_pid
      echo '关闭成功'
      break
    fi
    sleep 1
  done
}


if [[ -z "$alarmmain_pid" ]];then
  echo '未运行, 无需关闭'
else
  if [[ -z "$clean_disk_pid" ]];then
    kill -9 $alarmmain_pid
    echo '关闭成功'
  else
    stop_clean_disk_pid
  fi
fi
