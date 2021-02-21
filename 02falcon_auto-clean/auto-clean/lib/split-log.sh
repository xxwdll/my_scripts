#!/bin/bash
# date : 2021-01-19
split_file(){
  full_log_file=$1
  log_path=${full_log_file%/*}
  log_file=${full_log_file##*/}
  bak_time=$(date '+%Y-%m-%d-%H%M')
  bak_log_file=$log_file'-'$bak_time
  if [ -d $log_path ];then
    cd $log_path
    if [ -f $log_file ];then
      echo $log_file
      echo $bak_log_file
      #cp $log_file $bak_log_file && cat /dev/null > $log_file && gzip $bak_log_file
      cp $log_file $bak_log_file && cat /dev/null > $log_file
    else
      echo 'not exist!'
    fi
  fi
}

split_file '/home/auto-clean/log/alarm-clean.log'
