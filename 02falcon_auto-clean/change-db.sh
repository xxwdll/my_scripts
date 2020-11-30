#!/bin/bash
read -p "
1 : 插入数据
2 : 检索数据
==> " op

if [[ $op != "1" ]] && [[ $op != "2" ]];then
    echo "输入 1 或者 2"
    exit 1
fi

select_data(){
    read -p 'ip ==>' this_ip
    sqlite3 auto-clean.db "select * from app_info where ip='$this_ip'"
}
innsert_data(){
    read -p 'ip ==>' this_ip
    read -p 'way ==>' this_way
    read -p 'path ==>' this_path
    if [[ $this_way == "u03" ]];then
        this_command="[ -f "\"$this_path\"" ] && cat /dev/null > "$this_path
    fi
    echo $this_command
    sqlite3 auto-clean.db "innsert into app_info values('$this_ip','$this_way','\"$this_command\"');"
}


case $op in
    "1")
    innsert_data
    ;;
    "2")
    innsert_data
    ;;
    *)
    echo "异常..."
    break
    ;;
esac
