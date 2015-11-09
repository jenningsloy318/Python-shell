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
def sshcmd(server):
    try:
        print("Start to process "+server.rstrip()+"\n")
        log=open(log_file,"a")
        log.write("Start to process "+server.rstrip()+"\n\n")
        cmds = open(cmd_list)
        sshconn= paramiko.SSHClient()
        sshconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshconn.connect(hostname=server,username=user,password=passwd,timeout=50)
        for cmd in cmds:
            stdin, stdout, stderr = sshconn.exec_command(cmd)
            log.write(cmd)
            for err_line in stderr.readlines():
                print(err_line.rstrip())
                log.write(err_line+'\n')
            for line in stdout.readlines():
                log.write(line+"\n")
            log.write("\n")
        sshconn.close()
        print("Process "+server.rstrip()+" successfully \n")
        log.write("Process "+server.rstrip()+" successfully \n")
        log.flush()
        log.close()
        return True
    except paramiko.AuthenticationException as s:
        print(server.rstrip(),s.__str__(),"\n")
        log.write(s.__str__()+"\n")
        print("Process "+server.rstrip()+" failed \n")
        log.write("Process "+server.rstrip()+" failed \n")
        log.flush()
        log.close()
        return False
    except paramiko.SSHException as p:
        print(server.rstrip(),p.__str__(),"\n")
        log.write(p.__str__()+"\n")
        print("Process "+server.rstrip()+" failed \n")
        log.write("Process "+server.rstrip()+" failed \n")
        log.flush()
        log.close()
        return False
    except socket.error as t:
        print(server.rstrip(),t.__str__(),"\n")
        log.write(t.__str__()+"\n")
        print("Process "+server.rstrip()+" failed \n")
        log.write("Process "+server.rstrip()+" failed \n")
        log.flush()
        log.close()
        return False
def main():
    global log_file,cmd_list,user,passwd
    arguments = argparse.ArgumentParser()  
    arguments.add_argument("-s","--server_list",nargs="?",help="The servers list",required=True)
    arguments.add_argument("-c","--cmd_list",nargs="?",help="The command list",required=True)
    arguments.add_argument("-l","--log", nargs="?",help="The log file,default result.log",default="result.log")
    if len(sys.argv) ==1:
        arguments.print_help()
        sys.exit(1)
    args = arguments.parse_args()
    server_list = open(args.server_list)
    cmd_list = args.cmd_list
    log_file =args.log
    timestamp=time.strftime("%Y%m%d%H%M")
    user=input("Type the username to login: ")
    passwd=getpass.getpass()
    if os.path.exists(log_file):
        os.rename(log_file,log_file+"."+timestamp)
    hosts=server_list.readlines()
    start_time=datetime.datetime.now()
    print(start_time)
    pool = ThreadPool(20)
    pool.map(sshcmd,hosts)
    pool.close()
    pool.join()
    server_list.close()
    end_time=datetime.datetime.now()
    print(end_time)
    exit(0)
if __name__ == "__main__":
    main()
