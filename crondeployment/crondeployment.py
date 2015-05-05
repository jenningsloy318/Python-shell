#!/usr/bin/env python3
import os
import paramiko
import sys
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import argparse
import time
import datetime
import socket
import getpass
import mysqli
import mysql.connector
def generate_cvs(dplist_file):
    dplist = open(dplist_file,'w')    
    mysql_connection=mysql.connector.connect(user='',password='',host='',port='3408',database='onetool')
     for dp in dplist.readlines():
        DO_id_query=(select b.deploy_plan_id,a.cron_do_id,d.server_name,d.domain_name,d.server_ip,e.download_cmd,a.new_version,a.file_path as cvs_file_path,a.operation from itt_cron_do_file a inner join itt_cron_do b on a.cron_do_id=b.id inner join itt_cron_do_runtime c  on b.id = c.cron_do_id inner join itt_cron_server d  on c.cron_server = d.id inner join itt_vcs e on a.vcs_id =e.id where b.deploy_plan_id=7183 order by a.cron_do_id,d.domain_name;)

def main():
    global log_file,cmd_list,user,passwd
    arguments = argparse.ArgumentParser()  
    arguments.add_argument("-c","--cvs_list",nargs="?",help="The cvs  list")
    arguments.add_argument("-S","--server_name",nargs="?",help="us_cron/us_cron1/ukcron/xdcron/cacron/hyve_cron/hyve_cron1/mxcron/gis")
    arguments.add_argument("-D","--deploy_plan_id",nargs="?",help="deploy plan ID")
    if len(sys.argv) ==1:
        arguments.print_help()
        sys.exit(1)
    args = arguments.parse_args()
    cvs_list = open(args.cvs_list)
    判断是输入的server，然后链接数据库查询是否有DP，及是否有cron的DO，有的话就列出来，看选择是否部署
    判断输入的是DP， 然后链接数据库查询该DP所在的server和DO 进行确认

    根据server和DP，查询出相关cvs路径和实际路径进行checkout操作。
    循环操作，询问是否还要继续进行部署。

    server = args.server
    mysqli=.....

    dp
    for cvs_cmd in cvs_list.readline

    log_file =args.log
    timestamp=time.strftime("%Y%m%d%H%M")
    if os.path.exists(log_file):
        os.rename(log_file,log_file+"."+timestamp)
    hosts=server_list.readlines()
    start_time=datetime.datetime.now()
    print(start_time)
    server_list.close()
    end_time=datetime.datetime.now()
    print(end_time)
    exit(0)
if __name__ == "__main__":
    main()
