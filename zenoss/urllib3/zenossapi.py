#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-11-06 09:21:50

from urllib3 import HTTPConnectionPool
import json
import sys
class deviceapi(object):
    def __init__(self,zenoss_server,zenoss_username,zenoss_password):
        self.zenoss_server=zenoss_server
        self.username=zenoss_username
        self.password=zenoss_password
    def conn(self):
        self.loginParams={'came_fraaaaaom':'http://'+self.zenoss_server+':8080/zport/dmd',
                     '__ac_name':self.username,
                     '__ac_password':self.password,
                     'submitted':'true'
                    }
        self.reqheaders={'Content-Type':'application/json'}
        self.reqCount = 1
        self.pool=HTTPConnectionPool(self.zenoss_server,port=8080,maxsize=5)
        self.loginResponse=self.pool.request('POST','/zport/acl_users/cookieAuthHelper/login',fields=self.loginParams,redirect=False)
        self.cookie={'cookie': self.loginResponse.getheader('set-cookie')}
        return self.cookie
    def operate(self,action,method,datalist=[],cookie={}):
            self.routers = {    'MessagingRouter': 'messaging',
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

            self.cookie=cookie
            self.reqdata=[{
                            'type': 'rpc',
                            'data': datalist,
                            'method':method,
                            'action':action,
                            'tid':self.reqCount
                    }]
            self.reqCount +=1
            self.reqheaders.update(self.cookie)
            self.operateResponse=self.pool.urlopen('POST','/zport/dmd/'+self.routers[action]+'_router',body=json.dumps(self.reqdata),headers=self.reqheaders)
            if self.operateResponse.getheaders().getlist('Content-Type')[0] !='application/json':
                print('\033[1;31;47mLogin Failed, Please check your username and password !\033[0m')
                sys.exit(1)
            return self.operateResponse
