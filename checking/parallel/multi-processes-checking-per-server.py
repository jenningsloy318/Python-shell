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
        log_sshdcmd=open("/tmp/."+server.rstrip()+".log","w")
        log_sshdcmd.write("\n"+server.rstrip()+":Start to process "+server.rstrip()+"\n\n")
        cmds = open(cmd_list)
        sshconn= paramiko.SSHClient()
        sshconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshconn.connect(hostname=server,username=user,password=passwd,timeout=10)
        print("Login to "+server.rstrip()+" successfully\n")
        for cmd in cmds:
            stdin, stdout, stderr = sshconn.exec_command(cmd)
            log_sshdcmd.write(server.rstrip()+":"+cmd)
            print('The exit code of command <'+cmd.rstrip()+'> is: ',stdout.channel.recv_exit_status())
            print(server.rstrip()+":"+cmd)
            if stdout.channel.recv_exit_status() == 0:
                for line in stdout.readlines():
                    print(server.rstrip()+":"+line+"\n")
                    log_sshdcmd.write(server.rstrip()+":"+line+"\n")
                print('excute command <'+cmd.rstrip() +'> sucessfully')
            else:
                for out_line in stderr.readlines()+stdout.readlines():
                    print(server.rstrip()+':'+out_line+"\n")
                    log_sshdcmd.write(server.rstrip()+':'+out_line+'\n')
                print('\033[1;31;47mexcute command <'+cmd.rstrip()+'> failed\033[0m')
            log_sshdcmd.write("\n")
        sshconn.close()
        print("Process "+server.rstrip()+" Finished \n")
        log_sshdcmd.write(server.rstrip()+":Process "+server.rstrip()+" Finished \n")
        log_sshdcmd.flush()
        log_sshdcmd.close()
        return True
    except paramiko.AuthenticationException as s:
        print(server.rstrip(),s.__str__(),"\n")
        log_sshdcmd.write(server.rstrip()+" "+s.__str__()+"\n")
        print("Process "+server.rstrip()+" failed \n")
        log_sshdcmd.write(server.rstrip()+":Process "+server.rstrip()+" failed \n")
        log_sshdcmd.flush()
        log_sshdcmd.close()
        return False
    except paramiko.SSHException as p:
        print(server.rstrip(),p.__str__(),"\n")
        log_sshdcmd.write(server.rstrip()+" "+p.__str__()+"\n")
        print("Process "+server.rstrip()+" failed \n")
        log_sshdcmd.write(server.rstrip()+":Process "+server.rstrip()+" failed \n")
        log_sshdcmd.flush()
        log_sshdcmd.close()
        return False
    except socket.error as t:
        print(server.rstrip(),t.__str__(),"\n")
        log_sshdcmd.write(server.rstrip()+" "+t.__str__()+"\n")
        print("Process "+server.rstrip()+" failed \n")
        log_sshdcmd.write(server.rstrip()+":Process "+server.rstrip()+" failed \n")
        log_sshdcmd.flush()
        log_sshdcmd.close()
        return False
def main():
    global log_global_file,cmd_list,user,passwd
    arguments = argparse.ArgumentParser()  
    arguments.add_argument("-s","--server_list",nargs="?",help="The servers list")
    arguments.add_argument("-c","--cmd_list",nargs="?",help="The command list")
    arguments.add_argument("-l","--log", nargs="?",help="The log file,default result.log",default="result.log")
    if len(sys.argv) ==1:
        arguments.print_help()
        sys.exit(1)
    args = arguments.parse_args()
    server_list = open(args.server_list)
    cmd_list = args.cmd_list
    log_global_file =args.log
    timestamp=time.strftime("%Y%m%d%H%M")
    user=input("Type the username to login: ")
    passwd=getpass.getpass()
    if os.path.exists(log_global_file):
        os.rename(log_global_file,log_global_file+"."+timestamp)
    hosts=server_list.readlines()
    start_time=datetime.datetime.now()
    print(start_time)
    pool = ThreadPool(20)
    pool.map(sshcmd,hosts)
    pool.close()
    pool.join()
    log_global=open(log_global_file,"w")
    for host in hosts:
        if os.path.exists("/tmp/."+host.rstrip()+".log"):
            for line in open("/tmp/."+host.rstrip()+".log").readlines():
                log_global.write(line)
            os.remove("/tmp/."+host.rstrip()+".log")
    log_global.close()
    server_list.close()
    end_time=datetime.datetime.now()
    print(end_time)
    exit(0)
if __name__ == "__main__":
    main()
