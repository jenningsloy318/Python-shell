#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-06-25 08:45:22
import paramiko
import socket
class sshcmd(object):
    def __init__(self,ip,port,user,passwd,cmdlist,cmdlog):
        self.ip=ip
        self.port=port
        self.user=user
        self.passwd=passwd
        self.cmdlist=cmdlist
        self.cmdlog=cmdlog
    def run(self):
        try:
            sshconn= paramiko.SSHClient()
            sshconnlog=open(self.cmdlog,'w')
            print("Start to process "+self.ip.rstrip()+"\n")
            sshconnlog.write("\n"+self.ip.rstrip()+":Start to process "+self.ip.rstrip()+"\n\n")
            sshconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sshconn.connect(hostname=self.ip,port=self.port,username=self.user,password=self.passwd,timeout=10)
            for cmd in open(self.cmdlist):
                stdin, stdout, stderr = sshconn.exec_command(cmd)
                sshconnlog.write(self.ip.rstrip()+":"+cmd)
                print('The exit code of command <'+cmd.rstrip()+'> is: ',stdout.channel.recv_exit_status())
                print(self.ip.rstrip()+":"+cmd)
                if stdout.channel.recv_exit_status() == 0:
                    for line in stdout.readlines():
                        print(self.ip.rstrip()+":"+line+"\n")
                        sshconnlog.write(self.ip.rstrip()+":"+line+"\n")
                    print('excute command <'+cmd.rstrip() +'> sucessfully')
                else:
                    for out_line in stderr.readlines()+stdout.readlines():
                        print(self.ip.rstrip()+':'+out_line+"\n")
                        sshconnlog.write(self.ip.rstrip()+':'+out_line+'\n')
                    print('\033[1;31;47mexcute command <'+cmd.rstrip()+'> failed\033[0m')
            sshconnlog.write("\n")
            sshconn.close()
            print("Process "+self.ip.rstrip()+" successfully \n")
            sshconnlog.write(self.ip.rstrip()+":Process "+self.ip.rstrip()+" Finished \n")
            sshconnlog.flush()
       	    sshconnlog.close()
            return True
        except paramiko.AuthenticationException as s:
            print(self.ip.rstrip(),s.__str__(),"\n")
            sshconnlog.write(self.ip.rstrip()+" "+s.__str__()+"\n")
            print("\033[1;31;47mProcess "+self.ip.rstrip()+" failed \033[0m\n")
            sshconnlog.write(self.ip.rstrip()+":Process "+self.ip.rstrip()+" failed \n")
            sshconnlog.flush()
            sshconnlog.close()
            return False
        except paramiko.SSHException as p:
            print(self.ip.rstrip(),p.__str__(),"\n")
            sshconnlog.write(self.ip.rstrip()+" "+p.__str__()+"\n")
            print("\033[1;31;47mProcess "+self.ip.rstrip()+" failed \033[0m\n")
            sshconnlog.write(self.ip.rstrip()+":Process "+self.ip.rstrip()+" failed \n")
            sshconnlog.flush()
            sshconnlog.close()
            return False
        except socket.error as t:
            print(self.ip.rstrip(),t.__str__(),"\n")
            sshconnlog.write(self.ip.rstrip()+" "+t.__str__()+"\n")
            print("\033[1;31;47mProcess "+self.ip.rstrip()+" failed \033[0m\n")
            sshconnlog.write(self.ip.rstrip()+":Process "+self.ip.rstrip()+" failed \n")
            sshconnlog.flush()
            sshconnlog.close()
            return False
