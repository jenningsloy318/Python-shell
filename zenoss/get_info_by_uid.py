#!/usr/bin/env python2
from devices import zenoss_session

ZENOSS_INSTANCE = 'http://10.88.126.71:8080'
ZENOSS_USERNAME = 'admin'
ZENOSS_PASSWORD = 'passwd'

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
host_list='hosts.list'
for line in open(host_list):
    (IP,hostname,group)=line.split(",",3)
    uid='/zport/dmd/Devices/Server/Linux/devices/'+IP
    z=newsession.router_request('DeviceRouter', 'getInfo',
           data=[{'uid':uid}])['result']
for key in z['data'].keys():
    print key,z['data'][key]
