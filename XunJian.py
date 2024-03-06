#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Describe: 用于服务器资源巡检进行告警


import psutil
import os
import socket
from requests.models import ContentDecodingError


def getHostIP():
    """
    查询本机ip地址
    :return:
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()

    return ip


def getSystemInfo():
    system = os.uname()
    system_version = system.sysname
    system_info = "系统类型:%s" % system_version + '\n系统IP:\t%s' % getHostIP()
    return system_info


def getMemInfo():
    mem = psutil.virtual_memory()
    mem_total = mem.total / 1024 /1024 
    mem_free = mem.available / 1024 / 1024 
    mem_used = mem.used / 1024 /1024 
    mem_info = "内存共: %.2fM" % mem_total + '\n使用: %.2fM' % mem_used + '\n剩余: %.2fM' % mem_free
    return mem_info


def getDiskInfo():
    disk_system = psutil.disk_usage("/")
    disk_system_total = disk_system.total / 1024 / 1024 / 1024
    disk_system_free = disk_system.free / 1024 / 1024 / 1024
    disk_system_percent = disk_system.percent

    disk_app = psutil.disk_usage("/data")
    disk_app_total = disk_app.total / 1024 / 1024 / 1024
    disk_app_free = disk_app.free / 1024 / 1024 / 1024
    disk_app_percent = disk_app.percent
    disk_info = "/ 共:\t\t%dG" % disk_system_total + '\n/ 使用率:\t%.2f%%' % disk_system_percent + '\n/ 剩余:\t\t%dG' % disk_system_free + '\n/app 共:\t%dG' % disk_app_total + '\n/app 使用率:\t%.2f%%' % disk_app_percent + '\n/app 剩余:\t%dG' % disk_app_free
    return disk_info


def getCPUInfo():
    cpu_load = psutil.getloadavg()
    cpu_list = list(cpu_load)
    cpu_info = "CPU 平均05分钟负载: %.2f" % cpu_list[0] + '\nCPU 平均10分钟负载: %.2f' % cpu_list[1] + '\nCPU 平均15分钟负载: %.2f' % cpu_list[2]
    return cpu_info


def data():
    content=""
    content+=getSystemInfo()+"\n"+"-"*20+"\n"+getMemInfo()+"\n"+"-"*20+"\n"+getDiskInfo()+"\n"+"-"*20+"\n"+getCPUInfo()+"\n"
    return content


def sendDingMessage(content):
    import requests
    import json

    # 请求的URL，WebHook地址
    webhook = ""
    # 构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    # 构建请求数据
    message = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "atMobiles": [],
            "isAtAll": False
        }

    }
    # 对请求的数据进行json封装
    message_json = json.dumps(message)
    # 发送请求
    info = requests.post(url=webhook, data=message_json, headers=header)
    # 打印返回的结果
    # print(info.text)


def sendEmailMessage(content):
    import smtplib
    from email.mime.text import MIMEText

    smtp_server = "smtp.qq.com"
    smtp_port = 465

    sender_email = "xxxx@qq.com"
    sender_password = ""

    receiver_email = ""

    message = MIMEText(content, 'plain', 'utf-8')
    message["Subject"] = "告警"
    message["From"] = sender_email
    message["To"] = receiver_email

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, receiver_email, message.as_string())


if __name__ == '__main__':
    sendDingMessage(data())
    sendEmailMessage(data())