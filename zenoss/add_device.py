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
deviceClass='/zport/dmd/Devices'
new_host_list='hosts.list'
for line in open(new_host_list):
    (deviceIP,hostname,group)=line.split(",",3)
    newdevice=newsession.router_request('DeviceRouter', 'addDevice',data=[{'deviceName':deviceIP,'deviceClass':'/Server/Linux','title':hostname,'snmpCommunity':'Zenoss88','groupPaths':group,'model':'True'}])
    print newdevice
