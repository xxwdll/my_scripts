#!/bin/bash
t_ip=`/sbin/ifconfig | grep -oP 'inet.{1,9}([0-9]{1,3}\.){3}[0-9]{1,3}' | head -n 1 | grep -oP '([0-9]{1,3}\.){3}[0-9]{1,3}'`
disk_useage_percent(){
  this_path=$1
  disk_percent=$(df -h | grep -w "${this_path}$" | awk '{print $(NF-1)}' | grep -oP '[0-9]{1,3}')
  echo $disk_percent
  if [[ "$disk_percent" -ge 75 ]];then
    echo $this_path';;yes;;'$t_ip
  else
    echo 'pass'
  fi
}
