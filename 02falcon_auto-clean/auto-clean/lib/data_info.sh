#!/bin/bash
cd "$(dirname "$0")"

search_info(){
  read -p 'input ip==> ' this_ip
  echo -e '\n\n'

  this_sql="select cluster_info from app_info where ip='$this_ip'"
  this_clusters=$(sqlite3 auto-clean.db "$this_sql")
  for this_cluster in $this_clusters;
  do
    echo 'cluster_name==> '$this_cluster
    this_sql="select auto_key from cluster_info where cluster_name='$this_cluster'"
    keys=`sqlite3 auto-clean.db "$this_sql"`
    for li in `echo $keys`;
    do
      this_sql="select type_info from cluster_info where auto_key='$li' and cluster_name='$this_cluster'"
      this_path=`sqlite3 auto-clean.db "$this_sql"`
      echo 'key==> '$li ' path==> '$this_path
      this_sql="select command from cluster_info where auto_key='$li' and cluster_name='$this_cluster'"
      echo -e '\n--- command info ---'
      sqlite3 auto-clean.db "$this_sql"
    done
    echo '--- cluster info ---'
    this_sql="select ip from app_info where cluster_info='$this_cluster'"
    sqlite3 auto-clean.db "$this_sql"
    echo -e '\n'
  done

}

dev_null_fun(){
  read -p '文件名==> ' this_file_name
  read -p '集群名==> ' this_cluster_name
  read -p '根目录==> ' this_type_info
  this_sql="INSERT INTO "cluster_info" (cluster_name,type_info,command) VALUES('$this_cluster_name', '$this_type_info', 'this_file=''$this_file_name''
[ -f \$this_file ] && cat /dev/null > \$this_file');"
  echo $this_sql
  read -p 'input "Y" or "y" to continue: ' Isyes
  if [[ "$Isyes" == 'y' ]] || [[ "$Isyes" == 'Y' ]];then
    sqlite3 auto-clean.db "$this_sql"
    echo 'ok'
  else
    echo 'pass'
  fi
}

gzip_fun(){
  read -p '目录名==> ' this_dir_name
  read -p '集群名==> ' this_cluster_name
  read -p '根目录==> ' this_type_info
  this_sql="INSERT INTO "cluster_info" (cluster_name,type_info,command) VALUES('$this_cluster_name', '$this_type_info', 'this_dir=''$this_dir_name''
if [ -d \$this_dir ];then
  cd \$this_dir
  find ./ -cmin +60 -type f -name ''*20*'' | grep log | grep -v ''\.gz$'' | xargs -i gzip {}
fi');"
  echo $this_sql
  read -p 'input "Y" or "y" to continue: ' Isyes
  if [[ "$Isyes" == 'y' ]] || [[ "$Isyes" == 'Y' ]];then
    sqlite3 auto-clean.db "$this_sql"
    echo 'ok'
  else
    echo 'pass'
  fi
}

move_fun(){
  read -p '应用名==> ' this_app_name
  read -p '集群名==> ' this_cluster_name
  #read -p '根目录==> ' this_type_info
  this_sql="INSERT INTO "cluster_info" (cluster_name,type_info,command) VALUES('$this_cluster_name', '/u03', 'app_name=''$this_app_name''
this_ip=\$(ip addr | grep -A3 eth | grep inet | awk ''{print $2}'' | grep -oP ''([0-9]{1,3}\.){3}[0-9]{1,3}'')
src_dir=''/u03/backuplog/''\$app_name
tar_dir=''/mnt/hangyou/app/''\$app_name''/''\$this_ip
if [ -d \$src_dir ] && [ -d \$tar_dir ];then
  cd \$src_dir
  find ./ -mtime +30 -type f | grep 20 | grep log | xargs -i mv -f {} \$tar_dir
fi');"
  echo $this_sql
  read -p 'input "Y" or "y" to continue: ' Isyes
  if [[ "$Isyes" == 'y' ]] || [[ "$Isyes" == 'Y' ]];then
    sqlite3 auto-clean.db "$this_sql"
    echo 'ok'
  else
    echo 'pass'
  fi
}

add_info(){
  prompt_info="选择\n1==> 滞空\n2==> 压缩\n3==> 移动\n"
  echo -e $prompt_info
  read -p ':' num
  if [[ $num -eq 1 ]];then
    dev_null_fun
  elif [[ $num -eq 2 ]];then
    gzip_fun
  elif [[ $num -eq 3 ]];then
    move_fun 
  else
    echo 'pass'
  fi
}

delete_info(){
  read -p 'input key==> ' this_key
  this_sql='select * from cluster_info where auto_key='$this_key''
  sqlite3 auto-clean.db "$this_sql"
  read -p 'input "Y" or "y" to continue: ' Isyes
  if [[ "$Isyes" == 'y' ]] || [[ "$Isyes" == 'Y' ]];then
    this_sql='delete from cluster_info where auto_key='$this_key''
    sqlite3 auto-clean.db "$this_sql"
    echo 'ok'
  else
    echo 'pass'
  fi
}

while true;
do
  prompt_info="选择\n1==> 检索\n2==> 添加\n3==> 删除\n4==> 退出"
  echo -e $prompt_info
  read -p ':' num
  case $num in
    1)
      search_info
      ;;
    2)
      add_info
      ;;
    3)
      delete_info
      ;;
    4)
      exit 0
      ;;
    *)
      echo "pass"
      ;;
  esac
done
