#!/usr/bin/env python2
from zenossapi import deviceapi
import getpass
import argparse
import sys
import json

arguments = argparse.ArgumentParser()  
arguments.add_argument("-s","--server",nargs="?",help="The zenoss server ipaddress",required=True)
arguments.add_argument("-u","--user",nargs="?",help="The user of zenoss server,default is admin",default="admin")
arguments.add_argument("-f","--hostslist", nargs="?",help="The hosts list which will be deleted from zenoss",required=True)
if len(sys.argv) ==1:
   arguments.print_help()
   sys.exit(1)
args = arguments.parse_args()
passwd=getpass.getpass()


ZENOSS_SERVER = args.server
ZENOSS_USERNAME = args.user
ZENOSS_PASSWORD = passwd
newsession=deviceapi(ZENOSS_SERVER,ZENOSS_USERNAME,ZENOSS_PASSWORD)
conncookie=newsession.conn()
host_list=args.hostslist
for line in open(host_list):
    (deviceIP,hostname,OStype,group)=line.split(",",4)
    uid='/zport/dmd/Devices/Server/'+OStype+'/devices/'+deviceIP
    data=[{'uids':uid,'hashcheck':'','action':'delete'}]
    operation_result=newsession.operate('DeviceRouter', 'removeDevices',datalist=data,cookie=conncookie)
    result_info=json.loads(operation_result.data)['result']
    print deviceIP,':',result_info
