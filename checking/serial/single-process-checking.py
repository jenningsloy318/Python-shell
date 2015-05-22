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
def sshcmd(servername,server,user,passwd,port,cmd_list):
    try:
        print("Start to process "+server.rstrip()+"\n")
        log.write("\nStart to process "+servername+':'+server.rstrip()+"\n\n")
        cmds = open(cmd_list)
        sshconn= paramiko.SSHClient()
        sshconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #print(ord(passwd))
        sshconn.connect(hostname=server,port=port,username=user.rstrip(),password=passwd.rstrip(),timeout=10)
        print("Login to "+server.rstrip()+" successfully\n")
        log.write("Login to "+server.rstrip()+" successfully\n")

        for cmd in cmds:
            stdin, stdout, stderr = sshconn.exec_command(cmd)
            print('The exit code of command <'+cmd.rstrip()+'> is: ',stdout.channel.recv_exit_status())
            #print(stderr.readlines())
            log.write(cmd)
            if stdout.channel.recv_exit_status() == 0:
                for line in stdout.readlines():
                    print(line.rstrip())
                    log.write(line)
                print('excute command <'+cmd.rstrip() +'> sucessfully')
            else:
                for out_line in stderr.readlines()+stdout.readlines():
                    print(out_line.rstrip())
                    log.write(out_line)
                print('\033[1;31;47mexcute command <'+cmd.rstrip()+'> failed\033[0m')

            #print(stderr.readlines())
            #log.write(stderr.readlines())
            log.write("\n")
        sshconn.close()
        log.write("Process "+servername.rstrip()+':'+server.rstrip()+" Finished \n")
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
        if len(host_line) > 8:
            (host_name,hostip,user,passwd) = host_line.split(",",3)
            if hostip in ['10.88.126.88','192.168.18.131']:
                port=2222
            else:
                port=22
            if sshcmd(host_name,hostip,user,passwd,port,cmd_list):
               print("\nProcess "+host_name+':'+hostip.rstrip()+" successfully \n")
               print("-----------------------------------------------------------\n")
               log.flush()
            else:
               print("\nProcess "+host_name+':'+hostip.rstrip()+" failed \n")
               print("-----------------------------------------------------------\n")
               log.flush()
        else:
            continue
    log.close()
    end_time=datetime.datetime.now()
    print(end_time)
    exit(0)
if __name__ == "__main__":
    main()
