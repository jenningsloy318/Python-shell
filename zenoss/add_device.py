#!/usr/bin/env python2
from devices import zenoss_session
import getpass
import argparse
import sys

arguments = argparse.ArgumentParser()  
arguments.add_argument("-s","--server",nargs="?",help="The zenoss server ipaddress")
arguments.add_argument("-u","--user",nargs="?",help="The user of zenoss server  ",default="admin")
arguments.add_argument("-f","--hostslist", nargs="?",help="The hosts list which will be added to zenoss")
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
    deviceclass='/Server/'+OStype
    operation_result=newsession.router_request('DeviceRouter', 'addDevice',
			data=[{'deviceName':deviceIP,'deviceClass':deviceclass,'title':hostname,'snmpCommunity':'Zenoss88','groupPaths':group,'model':'True'}])
    print deviceIP,':',operation_result
