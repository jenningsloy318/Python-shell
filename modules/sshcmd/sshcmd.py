#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2016-02-11 12:49:35
import paramiko
import sys
import socket
class remotessh(object):
    def __init__(self):
        self.sshconn= paramiko.SSHClient()
        self.sshconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    def sshlogin(self,ipAddress,userName,passwWord,Port):
        self.ipAddress=ipAddress
        self.userName=userName
        self.passwWord=passwWord
        self.Port=Port
        try:
            print("Login to the server %s .\n "%self.ipAddress)
            self.sshconn.connect(hostname=self.ipAddress,username=self.userName,password=self.passwWord,timeout=10,port=self.Port)
            print("Login to the server %s successfully .\n "%self.ipAddress)
            self.sftp=self.sshconn.open_sftp()
            return True
        except paramiko.AuthenticationException as s:
            print(s)
            print("\033[1;31;47mLogin to the server %s failed,pls check your username/password\033[0m.\n "%self.ipAddress.strip())
            return False
        except paramiko.SSHException as p:
            print(p)
            print("\033[1;31;47mLogin to the server %s failed,the ssh2 protocol negotiation or logic error\033[0m.\n "%self.ipAddress.rstrip())
            return False
        except paramiko.BadHostKeyException as k:
            print(k)
            print("\033[1;31;47mLogin to the server %s failed,the ssh key can't be verified\033[0m.\n "%self.ipAddress.rstrip())
            return False
        except socket.error as t:
            print(t)
            print("\033[1;31;47mLogin to the server %s failed,the server can't be reached\033[0m.\n "%self.ipAddress.rstrip())
            return False

    def sshruncmd(self,cmd):
        stdin, stdout, stderr = self.sshconn.exec_command(cmd)
        outcontent=stdout.readlines()
        errorcontent=stderr.readlines()
        exit_code=stdout.channel.recv_exit_status() 
        print('%s: excuting command  \" %s \". \n'%(self.ipAddress,cmd.rstrip()))
        print('%s: The exit code of command %s  is : %s .\n'%(self.ipAddress,cmd.rstrip(),stdout.channel.recv_exit_status()))
        if exit_code == 0:
            print("%s: excute  command \"  %s \" successfully !\n"%(self.ipAddress,cmd.rstrip()))
            #for line in stdout.readlines():
            #    print('%s: %s.\n'%(self.ipAddress,line.rstrip()))
            result=outcontent
            return exit_code,result
        else:
            print('\033[1;31;47m%s: excute command %s failed\033[0m.\n'%(self.ipAddress,cmd.rstrip()))
            #for line in stderr.readlines()+stdout.readlines():
            #    print('%s: %s.\n'%(self.ipAddress,line.rstrip()))
            #print('%s out'%stdout.readlines())
            #print('%s error'%stderr.readlines())
            if len(outcontent) == 0:
                result=errorcontent
            else:
                result= ''.join([outcontent,errorcontent])
            return exit_code,result
    def sshupload(self,localpath,remotepath):
        print('Transfering local file: [ %s ] to remote  %s: [ %s ]\n'%(localpath,self.ipAddress,remotepath))
        self.sftp.put(localpath,remotepath)
    def sshdownload(self,remote,local):
        print('Downloading remote %s: [ %s ] to local: %s\n'%(self.ipAddress,remotepath,localpath))
        self.sftp.put(localpath,remotepath)
    def sshlogoff(self):
            self.sshconn.close()



