#!/bin/bash
i='1'
while true;
do
  if [[ $i == '4500' ]];then
    cat /dev/null > ./log/alarm-running.log
    i=1
    bash ./lib/update.sh >> ./log/alarm-update.log 2>&1
  else
    i=$[$i+1]
  fi
  echo 'check time ' `date` >> ./log/alarm-running.log
  # 从openfalcon 获取数据 执行清理操作
  bash ./lib/falcon-clean-disk.sh >> ./log/alarm-clean.log 2>&1
  sleep 15
done
