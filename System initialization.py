#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Describe: Linux系统安装完成后，对于系统的初始化工作

import subprocess

def Usage():
    print("""
        1. 配置/修改网卡IP
        2.系统初始化（适用于CentOS、RedHat）
    """)

 
class NetworkConfigure():
    
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
                
            with open(f'/etc/sysconfig/network-scripts/ifcfg-{interface}', 'w') as file:
                 file.writelines(lines)

            print(f'网卡：{interface} 网卡IP地址:{ip} 子网掩码:{netmask} 网关:{gateway}')

            subprocess.run(['systemctl', 'restart', 'network'])

        except Exception as e:
            print(f'Error occurred: {e}')


class SystemConfigure():
    
    # 关闭系统防火墙
    def disable_firewalld(self):
        subprocess.run(['systemctl', 'disable', 'firewalld'])
        subprocess.run(['systemctl', 'stop', 'firewalld'])

    # 关闭SELINUX
    def disable_selinux(self):
        subprocess.run(['setenforce', '0'])
        with open('/etc/selinux/config','r') as file:
            lines = file.readlines()
            
        for i, line in enumerate(lines):
            if line.startswith('SELINUX='):
                lines[i] = f'SELINUX=disabled'

        with open('/etc/selinux/config', 'w') as file:
            file.writelines(lines)

    # 修改最大文件句柄数限制
    def ulimit(self):
        subprocess.run(['ulimit ', '-n', '65535'])
        try:
            with open('/etc/security/limits.conf', 'a') as file:
                file.write("* soft nofile 65535\n")
                file.write("* hard nofile 65536\n")
                file.write("* soft nproc 4096\n")
                file.write("* hard nproc 4096\n")

            subprocess.run(['/sbin/sysctl', '-p'])

        except Exception as e:
            print(f'Error occurred: {e}')

    # 增加内核参数
    def set_kernel_parameters(self):
        sysctl_conf_path = '/etc/sysctl.conf'

        params_to_add = [
            "net.ipv4.tcp_fin_timeout = 30",
            "net.ipv4.tcp_keepalive_time = 1200",
            "net.ipv4.tcp_syncookies =1",
            "net.ipv4.tcp_tw_reuse = 1",
            "net.ipv4.tcp_tw_recycle =1",
            "net.ipv4.ip_local_port_range = 10000 65000",
            "net.ipv4.tcp_max_syn_backlog = 8192",
            "net.ipv4.tcp_max_tw_buckets = 5000",
        ]

        try:
            with open(sysctl_conf_path, 'r') as file:
                existing_content = file.read()
            
            with open(sysctl_conf_path, 'a') as file:
                for params in params_to_add:
                    if params not in existing_content:
                        file.write(params + '\n')
            print("Parameters added to sysctl.conf successfully.")

            subprocess.run(['/sbin/sysctl', '-p'])

        except FileNotFoundError:
            print(f'Error: {sysctl_conf_path} not found.')
        except PermissionError:
            print(f'Error: Permission denied to access {sysctl_conf_path}.')
        except Exception as e:
            print(f'Error occurred: {e}')


        
        
            

def main():
    Usage()
    num = int(input('请输入功能选项：' ))
    if num == int(1):
        networkconfigure = NetworkConfigure()
        networkconfigure.input_ipaddress()
    elif num == int(2):
        systemconfigure = SystemConfigure()
        systemconfigure.disable_firewalld()
        systemconfigure.disable_selinux()
        systemconfigure.ulimit()
        systemconfigure.set_kernel_parameters()
    else:
        print("Invalid option.")
        Usage()
        num = int(input('请输入功能选项：' ))
            

if __name__ == '__main__': 
    main()