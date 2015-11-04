#!/usr/bin/env python2
from devices import zenoss_session
import getpass
import argparse
import sys

arguments = argparse.ArgumentParser()  
arguments.add_argument("-s","--server",nargs="?",help="The zenoss server ipaddress")
arguments.add_argument("-u","--user",nargs="?",help="The user of zenoss server",default="admin")
arguments.add_argument("-f","--hostslist", nargs="?",help="The hosts list  which we will get the info for ")
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
host_list=args.hostslist
for line in open(host_list):
    (deviceIP,hostname,OStype,group)=line.split(",",4)
    uid='/zport/dmd/Devices/Server/'+OStype+'/devices/'+deviceIP
    operation_result=newsession.router_request('DeviceRouter', 'getInfo',data=[{'uid':uid}])['result']
    if operation_result['success']:
        for key in operation_result['data'].keys():
            print deviceIP,':',key,':',operation_result['data'][key]
    else:
        print deviceIP,':',operation_result
