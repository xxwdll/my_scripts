#!/bin/bash
cd "$(dirname "$0")"
date
echo 'check...'

result_get=`./get_app_info.py`
result1=`echo $result_get | awk '{print $1}'`
result2=`cat app_info.txt | wc -l`

echo $result1

result3=`sqlite3 auto-clean.db "select count(*) from app_info_temp"`

txt2sqlite(){
sqlite3 auto-clean.db << EOF
drop table if exists app_info_temp;
CREATE TABLE "app_info_temp" (
  "ip",
  "cluster_info",
  "app_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
);
.quit
EOF

  cat app_info.txt | while read li;
  do
    v1=` echo $li | awk '{print $1}'`
    v2=` echo $li | cut -d\  -f2-`
    this_sql="insert into app_info_temp (ip, cluster_info) values('$v1','$v2');"
    sqlite3 auto-clean.db "$this_sql"
  done
  echo 'update data==>'
  this_sql='SELECT a.ip, a.cluster_info
  FROM
  app_info_temp AS a
  LEFT JOIN app_info AS b
  ON (a.ip = b.ip AND a.cluster_info = b.cluster_info)
  WHERE b.ip ISNULL;'
  sqlite3 auto-clean.db "$this_sql"

  this_sql='insert into app_info (ip, cluster_info)
  SELECT a.ip, a.cluster_info
  FROM
  app_info_temp AS a
  LEFT JOIN app_info AS b
  ON (a.ip = b.ip AND a.cluster_info = b.cluster_info)
  WHERE b.ip ISNULL;'
  sqlite3 auto-clean.db "$this_sql"
}

if [[ "$result1" == "ok" ]];then
  if [[ "$result2" != "$result3" ]];then
    echo 'need update..'
    bak_time=`date +'%Y%m%d%H'`
    cp ./auto-clean.db ../bak/auto-clean.db${bak_time}
    txt2sqlite
  else
    echo 'pass'
  fi
else
  echo 'update later..'
fi

