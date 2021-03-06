#!/bin/bash
# author 021786
# date 2020-09-16

today="%"$(date "+%Y-%m-%d")"%"
yesterday="%"$(date "+%Y-%m-%d" --date='-1 day')"%"

this_sql='select endpoint, metric, priority, current_step, timestamp, note \
from event_cases \
where \
status = "PROBLEM" \
and \
-- (endpoint not like "%自维%" and endpoint not like "%网络组%" and endpoint not like "%企业组%" and endpoint not like "%春秋旅游%") \
(timestamp like "'$today'" or timestamp like "'$yesterday'") \
order by timestamp desc limit 100;'

#echo $this_sql
ssh remote_ip "mysql -uroot -pPASSWORD -Dalarms -e'$this_sql'" | while read li;
do
  echo $li
  this_ip=`echo $li | awk '{print $1}' | awk -F '-' '{print $NF}'`
  echo $this_ip
done
