#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Describe: Linux系统安装完成后，对于系统的初始化工作

import subprocess

class NetworkConfigure(object):
    
    def input_ipaddress(self):
            new_interface = input('网卡名称：')
            new_ip = input("新IP地址:")
            new_netmask = input("新子网掩码:")
            new_gateway = input("新网关:")
            self.set_ipaddress(new_interface, new_ip, new_netmask, new_gateway)
            

    def set_ipaddress(self, interface, ip, netmask, gateway='0.0.0.0'):
        try:
            # 读取网卡配置文件
            with open(f'/etc/sysconfig/network-scripts/ifcfg-{interface}', 'r') as file:
                lines = file.readlines()

            ipaddr_exists = False
            gateway_exists =False
            netmask_exists = False

            # 修改ip、网关参数
            for i, line in enumerate(lines):
                if line.startswith('BOOTPROTO'):
                     lines[i] = f'BOOTPROTO=static\n'
                elif line.startswith('ONBOOT'):
                     lines[i] = f'ONBOOT=yes\n'
                elif line.startswith('IPADDR'):
                    lines[i] = f'IPADDR={ip}\n'
                    ipaddr_exists = True
                elif line.startswith('NETMASK'):
                    lines[i] = f'NETMASK={netmask}\n'
                    netmask_exists = True
                elif line.startswith('GATEWAY'):
                    lines[i] = f'GATEWAY={gateway}\n'
                    gateway_exists = True
                
            if not ipaddr_exists:
                lines.append(f'IPADDR={ip}\n')
            if not netmask_exists:
                lines.append(f'NETMASK={netmask}\n')
            if not gateway_exists:
                lines.append(f'GATEWAY={gateway}\n')

            # 将修改后的配置写回文件
            with open(f'/etc/sysconfig/network-scripts/ifcfg-{interface}', 'w') as file:
                 file.writelines(lines)

            print(f'网卡：{interface} 网卡IP地址:{ip} 子网掩码:{netmask} 网关:{gateway}')

            subprocess.run(['systemctl', 'restart', 'network'])

        except Exception as e:
            print(f'Error occurred: {e}')


def SystemConfigure():
    # 关闭系统防火墙
    subprocess.run(['systemctl', 'disable', 'firewalld'])
    subprocess.run(['systemctl', 'stop', 'firewalld'])

    # 关闭SELINUX
    subprocess.run(['setenforce', '0'])
    with open('/etc/selinux/config','r') as file:
        lines = file.readlines()
        
    for i, line in enumerate(lines):
        if line.startswith('SELINUX='):
            lines[i] = f'SELINUX=disabled'

    with open('/etc/selinux/config', 'w') as file:
        file.writelines(lines)

    # 修改最大文件句柄数限制
    subprocess.run(['ulimit ', '-n', '65535'])
    with open('/etc/security/limits.conf', 'a') as file:
         file.write("* soft nofile 65535\n")
         file.write("* hard nofile 65536\n")
         file.write("* soft nproc 4096\n")
         file.write("* hard nproc 4096\n")
    
    with open('/etc/sysctl.conf', 'a') as file:
         file.write("fs.file-max=655350\n")
    subprocess.run(['/sbin/sysctl', '-p'])
     

def main():
        num = int(input('请输入功能选项：' ))
        if num == int(1):
             configure = NetworkConfigure()
             configure.input_ipaddress()
            

if __name__ == '__main__': 
    main()