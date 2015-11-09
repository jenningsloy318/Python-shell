#!/usr/bin/env python3
from zenossapi import deviceapi
import getpass
import argparse
import sys
import json

arguments = argparse.ArgumentParser()  
arguments.add_argument("-s","--server",nargs="?",help="The zenoss server ipaddress",required=True)
arguments.add_argument("-u","--user",nargs="?",help="The user of zenoss server,default is admin",default="admin")
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
deviceClass='/zport/dmd/Devices'
data=[{'uid': deviceClass,'params': {},'limit':10000 }]
operation_result=newsession.operate('DeviceRouter','getDevices',datalist=data,cookie=conncookie)
devlist=(json.loads(bytes.decode(operation_result.data))['result']['devices'])
for devid in range(len(devlist)):
    print(devid+1,devlist[devid]['uid'])
