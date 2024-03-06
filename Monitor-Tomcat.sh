#!/bin/bash
# Describe: 用于监听Tomcat进程是否存在或者假死，状态不正常自动重启，配合cron使用

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

export JAVA_HOME="/app/jdk1.8.0_301"
export JRE_HOME="/app/jdk1.8.0_301/jre"
export CLASSPATH=.:$JAVA_HOME/jre/lib:$JAVA_HOME/lib:$JAVA_HOME/lib/tools.jar
export PATH=$JAVA_HOME/bin:$JRE_HOME:/app/nginx/sbin:$PATH

TomcatID=$(ps -ef|grep tomcat|grep -v grep|awk -F" " '{print $2}')

StartTomcat="/app/tomcat/bin/startup.sh"

WebUrl=http://localhost:8080

GetPageInfo=/app/Monitor/Tomcat-Monitor.Info

TomcatMonitorLog=/app/Monitor/Tomcat-Monitor.log

Monitor()
{
        echo "[info]开始监控Tomcat...[$(date +'%F %H:%M:%S')]"
        if [ ${TomcatID} ];then
          TomcatServiceCode=$(curl -o ${GetPageInfo} -s -m 10 --connect-timeout 10 -w %{http_code} -k ${WebUrl})
          if [ ${TomcatServiceCode} -eq 200 ];then
            echo "[info]页面返回码为${TomcatServiceCode},Tomcat启动成功,测试页面正常......"
          else
            echo "[error]Tomcat页面出错,请注意......状态码为${TomcatServiceCode},错误日志已输出到${GetPageInfo}"
            echo "[error]页面访问出错,开始重启Tomcat"
            kill -9 ${TomcatID}
            sleep 3
    
            ${StartTomcat}
          fi
        else
          echo "[error]Tomcat进程不存在!Tomcat开始自动重启..."
          echo "[info]${StartTomcat},请稍候......"
          
          ${StartTomcat}
        fi
}

def main()
  Monitor>>${TomcatMonitorLog}


main
