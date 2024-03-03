#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Describe: MySQL 数据库备份

import datetime
import subprocess
import os

def mysql_backup():
    # mysql 信息
    mysql_host = 'localhost'
    mysql_user = 'root'
    mysql_password = 'admin@123'
    mysql_database = 'djaogo-demo1'

    # 备份文件保存路径
    backup_dir = '/opt/mysql_backup'

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    backup_file = f'{mysql_database}_{current_time}.sql.gz'

    backup_path = os.path.join(backup_dir, backup_file)

    backup_command = f'mysqldump --host={mysql_host} --user={mysql_user} --password={mysql_password} {mysql_database} | gzip > {backup_path}'

    try:
        subprocess.run(backup_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error occurred during MySQL backup: {e}')
        