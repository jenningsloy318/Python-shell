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
z=newsession.router_request('DeviceRouter', 'getDevices',
                                    data=[{'uid': deviceClass,
                                        'params': {},'limit':10000 }])['result']
for dev in range(len(z['devices'])):
    print dev,z['devices'][dev]
