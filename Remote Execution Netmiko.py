#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Describe: Netmiko版，在windows端远程批量获取远程主机信息，或批量执行远程主机脚本

from netmiko import ConnectHandler

def ssh_cmd(ip, port, username, password, cmd='ls -l', device_type="linux"):
    try:
        conn = ConnectHandler(ip=ip,
                              port=port,
                              username=username,
                              password=password,
                              device_type=device_type)
        conn.enable()
        output = conn.send_command(cmd)
        conn.disconnect()

        return output
        
    except Exception as e:
        print(f'命令执行错误{e}')
        return None

def main():
    hosts = [
        {'ip': '192.168.1.1', 'port': 22, 'username': 'root', 'password': '!ColasoftL23'},
        {'ip': '192.168.1.2', 'port': 22, 'username': 'root', 'password': '!ColasoftL23'},
    ]

    cmd = 'df -h'

    for host in hosts:
        try:
            result = ssh_cmd(**host, cmd=cmd)
            # print(f"主机{host['ip']}的执行结果")
            # print(result)
            with open('./ssh_cmd_result.txt', 'a', encoding='utf-8') as file:
                file.write(f"主机{host['ip']}的执行结果 \n {result} \n\n")
        except Exception as e:
            print(f'Error occurred: {e}')

if __name__ == "__main__":
    main()
