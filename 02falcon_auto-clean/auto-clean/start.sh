#!/bin/bash

this_pid=`ps -ef | grep alarm-main.sh | grep -v grep | awk '{print $2}'`

if [[ ! -z "$this_pid" ]];then
  echo '正在运行..'
else
  bash alarm-main.sh &
  echo 'falcon 清理启动..'
fi


this_pid=`ps -ef | grep active-main.sh | grep -v grep | awk '{print $2}'`

if [[ ! -z "$this_pid" ]];then
  echo '正在运行..'
else
  bash activeClean/active-main.sh &
  echo '主动清理启动..'
fi

