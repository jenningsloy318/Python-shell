#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-12-07 14:32:32
import paramiko
class sftp_server(object):
    def __init__(self,host,user,passwd,port=22):
        self.transport=paramiko.Transport((host,port))
        try:
            self.transport.connect(username=user,password=passwd)
        except paramiko.SSHException: 
            print("Login failed")
        self.sftp=paramiko.SFTPClient.from_transport(self.transport)
    def download(self,remotefile,localfile):
        self.sftp.get(remotefile,localfile)
    def upload(self,remotefile,localfile):
        self.sftp.upload(localfile,remotefile)
    def logoff(self):
        self.sftp.close()
