#!/bin/bash
# Describe: 用于删除MySQL数据库临时查询时产生的临时表

host=$1
user=$2
password=$3

mysql -u用户 -p密码 -h主机IP -e "use db_name;show tables;" | grep "^tmp*" > /tmp/temp.txt;
cat /tmp/temp.txt | xargs -I{} mysql -u${user} -p${password} -h${host} -e "use db_name;drop table {};"

