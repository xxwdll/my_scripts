#!/bin/bash

stop_by_pid(){
  main_name=$1
  exec_name=$2
  main_pid=`ps -ef | grep $main_name | grep -v grep | awk '{print $2}'`
  exec_pid=`ps -ef | grep $exec_name | grep -v grep | awk '{print $2}'`
  if [[ ! -z "$main_pid" ]];then
    if [[ -z "$exec_pid" ]];then
      echo $main_name 'kill ...'
      kill -9 $main_pid
    else
      while true:
        do
          echo $exec_name 'kill ...'
          exec_pid=`ps -ef | grep $exec_name | grep -v grep | awk '{print $2}'`
          if [[ -z "$exec_pid" ]];then
            echo $main_name 'kill ...'
            kill -9 $main_pid
            break
          fi
          sleep 1
        done
    fi
  fi
  echo 'ok'
}

stop_by_pid "alarm-main.sh" "falcon-clean-disk.sh"
stop_by_pid "active-main.sh" "clean-active.sh"
