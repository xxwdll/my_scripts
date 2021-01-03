#!/bin/bash

this_pid=`ps -ef | grep alarm-main.sh | grep -v grep | awk '{print $2}'`

if [[ ! -z "$this_pid" ]];then
  echo '正在运行..'
else
  bash alarm-main.sh &
  echo '启动..'
fi
