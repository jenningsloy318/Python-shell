#!/usr/bin/env python2
from devices import zenoss_session
import getpass
import argparse
import sys


arguments = argparse.ArgumentParser()  
arguments.add_argument("-s","--server",nargs="?",help="The zenoss server ipaddress")
arguments.add_argument("-u","--user",nargs="?",help="The user of zenoss server  ")
if len(sys.argv) ==1:
   arguments.print_help()
   sys.exit(1)
args = arguments.parse_args()
passwd=getpass.getpass()


ZENOSS_INSTANCE = 'http://'+args.server+':8080'
ZENOSS_USERNAME = args.user
ZENOSS_PASSWORD = passwd

ROUTERS = { 'MessagingRouter': 'messaging',
            'EventsRouter': 'evconsole',
            'ProcessRouter': 'process',
            'ServiceRouter': 'service',
            'DeviceRouter': 'device',
            'NetworkRouter': 'network',
            'TemplateRouter': 'template',
            'DetailNavRouter': 'detailnav',
            'ReportRouter': 'report',
            'MibRouter': 'mib',
            'ZenPackRouter': 'zenpack' }

newsession=zenoss_session(ZENOSS_USERNAME,ZENOSS_PASSWORD,ZENOSS_INSTANCE,ROUTERS)
deviceClass='/zport/dmd/Devices'
operation_result=newsession.router_request('DeviceRouter', 'getDevices',data=[{'uid': deviceClass,'params': {},'limit':10000 }])['result']
for devID in range(len(operation_result['devices'])):
    print devID,operation_result['devices'][devID]
