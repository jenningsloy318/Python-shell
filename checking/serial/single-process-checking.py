#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import paramiko
import sys
import argparse
import time
import datetime
import socket
import codecs
def sshcmd(servername,server,user,passwd,cmd_list):
    try:
        print("Start to process "+server.rstrip()+"\n")
        log.write("\nStart to process "+servername+':'+server.rstrip()+"\n\n")
        cmds = open(cmd_list)
        sshconn= paramiko.SSHClient()
        sshconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #print(ord(passwd))
        sshconn.connect(hostname=server,username=user.rstrip(),password=passwd.rstrip(),timeout=10)
        for cmd in cmds:
            stdin, stdout, stderr = sshconn.exec_command(cmd)
            #print(stderr.readlines())
            log.write(cmd)
            #print(stderr.readlines())
            #log.write(stderr.readlines())
            for err_line in stderr.readlines():
                print(err_line.rstrip())
                log.write(err_line+'\n')
            for line in stdout.readlines():
                log.writelines(line.rstrip()+'\n')
            log.write("\n")
        sshconn.close()
        log.write("Process "+servername.rstrip()+':'+server.rstrip()+" successfully \n")
        log.write("################################################################ \n")
        return True
    except paramiko.AuthenticationException as s:
        print(server.rstrip(),s.__str__(),"\n")
        log.write(server.rstrip()+" "+s.__str__()+"\n")
        print("Process "+servername.rstrip()+':'+server.rstrip()+" failed \n")
        log.write("Process "+servername.rstrip()+':'+server.rstrip()+" failed \n")
        log.write("################################################################ \n")
        log.flush()
        return False
    except paramiko.SSHException as p:
        print(server.rstrip(),p.__str__(),"\n")
        log.write(servername.rstrip()+':'+server.rstrip()+" "+p.__str__()+"\n")
        print("Process "+servername.rstrip()+':'+server.rstrip()+" failed \n")
        log.write("Process "+servername.rstrip()+':'+server.rstrip()+" failed \n")
        log.write("################################################################ \n")
        log.flush()
        return False
    except socket.error as t:
        print(server.rstrip(),t.__str__(),"\n")
        log.write(servername.rstrip()+':'+server.rstrip()+" "+t.__str__()+"\n")
        print("Process "+servername.rstrip()+':'+server.rstrip()+" failed \n")
        log.write("Process "+servername.rstrip()+':'+server.rstrip()+" failed \n")
        log.write("################################################################ \n")
        log.flush()
        print(server.rstrip(),t)
        return False 
def main():
    global log 
    arguments = argparse.ArgumentParser()  
    arguments.add_argument("-s","--server_list",nargs="?",help="The servers list")
    arguments.add_argument("-c","--cmd_list",nargs="?",help="The command list")
    arguments.add_argument("-l","--log", nargs="?",help="The log file,default result.log",default="result.log")
    if len(sys.argv) ==1:
        arguments.print_help()
        sys.exit(1)
    args = arguments.parse_args()
    server_list = args.server_list
    cmd_list = args.cmd_list
    log_file = args.log
    timestamp=time.strftime("%Y%m%d%H%M")
    if os.path.exists(log_file):
        os.rename(log_file,log_file+"."+timestamp)
    log = open(log_file,"w")
    start_time=datetime.datetime.now()
    print(start_time)
    #for hostip in open(server_list):
    for host_line in open(server_list):
        (host_name,hostip,user,passwd) = host_line.split(",",3)
        if sshcmd(host_name,hostip,user,passwd,cmd_list):
           print("\nProcess "+host_name+':'+hostip.rstrip()+" successfully \n")
           print("-----------------------------------------------------------\n")
           log.flush()
        else:
           print("\nProcess "+host_name+':'+hostip.rstrip()+" failed \n")
           print("-----------------------------------------------------------\n")
           log.flush()
    log.close()
    end_time=datetime.datetime.now()
    print(end_time)
    exit(0)
if __name__ == "__main__":
    main()
