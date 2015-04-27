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
def main():
    global log_file,cmd_list,user,passwd
    arguments = argparse.ArgumentParser()  
    arguments.add_argument("-c","--cvs_list",nargs="?",help="The cvs  list")
    arguments.add_argument("-l","--log", nargs="?",help="The log file,default result.log",default="result.log")
    if len(sys.argv) ==1:
        arguments.print_help()
        sys.exit(1)
    args = arguments.parse_args()
    cvs_list = open(args.cvs_list)
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
