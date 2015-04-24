#!/usr/bin/env python3
import os
import paramiko
import threading
import sys
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import argparse
import time
import datetime
import time
import socket

def sshcmd(server,user,passwd,cmd_list):
    try:
        print('Start to process '+server.rstrip()+'\n')
        log.write('\nStart to process '+server.rstrip()+'\n\n')
        cmds = open(cmd_list)
        sshconn= paramiko.SSHClient()
        sshconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshconn.connect(hostname=server,username=user,password=passwd,timeout=10)
        for cmd in cmds:
            stdin, stdout, stderr = sshconn.exec_command(cmd)
            log.write(cmd)
            for line in stdout.read():
                log.writelines(line)
            log.write('\n')
        sshconn.close()
        log.write('Process '+server.rstrip()+' successfully \n')
        return True
    except paramiko.AuthenticationException as s:
        print(server.rstrip(),s.__str__(),'\n')
        log.write(server.rstrip()+' '+s.__str__()+'\n')
        print('Process '+server.rstrip()+' failed \n')
        log.write('Process '+server.rstrip()+' failed \n')
        log.flush()
        return False
    except paramiko.SSHException as p:
        print(server.rstrip(),p.__str__(),'\n')
        log.write(server.rstrip()+' '+p.__str__()+'\n')
        print('Process '+server.rstrip()+' failed \n')
        log.write('Process '+server.rstrip()+' failed \n')
        log.flush()
        return False
    except socket.error as t:
        print(server.rstrip(),t.__str__(),'\n')
        log.write(server.rstrip()+' '+t.__str__()+'\n')
        print('Process '+server.rstrip()+' failed \n')
        log.write('Process '+server.rstrip()+' failed \n')
        log.flush()
        print(server.rstrip(),t)
        return False 
def main():
    global log 
    arguments = argparse.ArgumentParser()  
    arguments.add_argument('-s','--server_list',nargs='?',help='The servers list')
    arguments.add_argument('-c','--cmd_list',nargs='?',help='The command list')
    arguments.add_argument('-l','--log', nargs='?',help='The log file,default result.log',default='result.log')
    if len(sys.argv) ==1:
        arguments.print_help()
        sys.exit(1)
    args = arguments.parse_args()
    server_list = args.server_list
    cmd_list = args.cmd_list
    log_file = args.log
    timestamp=time.strftime('%Y%m%d%H%M')
    if os.path.exists(log_file):
        os.rename(log_file,log_file+'.'+timestamp)
    log = open(log_file,'w')
    start_time=datetime.datetime.now()
    print(start_time)
    for hostip in open(server_list):
   #for hostline in open(server_list):
   #(hostname,hostip,user,passwd) = host_line.split(",",3)
        if sshcmd(hostip,'user','passwd',cmd_list):
            print('\nProcess '+hostip.rstrip()+' successfully \n')
            log.flush()
        else:
            print('\nProcess '+hostip.rstrip()+' failed \n')
            log.flush()
    else:
        print ('All servers are processed !')
        log.close()
    end_time=datetime.datetime.now()
    print(end_time)
    exit(0)
if __name__ == '__main__':
    main()
