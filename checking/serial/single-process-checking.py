#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2016-02-11 18:54:16
import argparse
import configparser
import sys
import getpass
from sshcmd import remotessh

if __name__ == "__main__":
###To out put the comand help 
    arguments = argparse.ArgumentParser()  
    arguments.add_argument("-c","--config",nargs="?",help="Config file",required=True)
    if len(sys.argv) ==1:
        arguments.print_help()
        sys.exit(1)
    args = arguments.parse_args()
    
##To process the configuration file    
    config = configparser.ConfigParser()
    configfile=open(args.config)
    config.read_file(configfile)
    server_list=config['server-list']['server-list']
    solaris_cmd_list=config['cmmmand-list']['solaris-cmds']
    linux_cmd_list=config['cmmmand-list']['linux-cmds']
    logfile=config['log']['logfile']
    if config['account']['username']:
        username=config['account']['username']
    if config['account']['password']:
        password=config['account']['password']
    configfile.close()
    
    checkinglog=open(logfile,'w')

## get the host/user/password info from host list if user/password are not set in the cofig file
    for host_line in open(server_list):
        host_info=host_line.split(',')
        if len(host_info) ==4:
            hostname=host_info[0].strip()
            ip=host_info[1].strip()
            username=host_info[2].strip()
            password=host_info[3].strip()
        elif len(host_info) ==1:
            ip=host_info[0].strip()
        else:
            print('Wrong host file format,pls check again')

## set the ssh port 

        if ip in ['10.88.126.88','192.168.18.131']:
            port=2222
        else:
            port=22

## login to the server and check if it is solairs or linux, and then set the command list
        ssh=remotessh(ip,username,password,port)
        checkinglog.write('Login to %s successfully.\n'%ip)
        ssh.sshlogin()
        osType=ssh.sshruncmd('uname')
        if osType[0]==0 and osType[1][0].strip() =='Linux':
            cmd_list=linux_cmd_list
        else:
            cmd_list=solaris_cmd_list

## running the check command on remote server
        checkinglog.write('Checking Begins:\n')
        for cmd in cmd_list.split(','):
            checkinglog.write(cmd+'\n\n')
            run_result=ssh.sshruncmd(cmd)
            for run_result_detail in run_result[1]:
                checkinglog.write(run_result_detail)
                print('%s :%s'%(ip,run_result_detail))
            checkinglog.write('\n')
        checkinglog.flush()
    checkinglog.close()
    




