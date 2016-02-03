#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-11-06 09:21:50
import pycurl
from urllib.parse import urlencode
import json
import sys
from io import BytesIO
import re

class deviceapi(object):
    def __init__(self,zenoss_server,zenoss_username,zenoss_password):
        self.zenoss_server=zenoss_server
        self.username=zenoss_username
        self.password=zenoss_password
    def login(self):
        self.login_url='http://'+self.zenoss_server+':8080/zport/acl_users/cookieAuthHelper/login'
        self.curl=pycurl.Curl()
        self.curl.setopt(self.curl.URL,self.login_url)
        self.curl.setopt(self.curl.POST,1)
        self.login_para={'came_from':'http://'+self.zenoss_server+':8080/zport/dmd/','submitted':'true','__ac_name':self.username,'__ac_password':self.password}
        self.curl.setopt(self.curl.POSTFIELDS,urlencode(self.login_para))
        login_buffer=BytesIO()
        self.curl.setopt(self.curl.WRITEDATA,login_buffer)
        self.curl.setopt(self.curl.FOLLOWLOCATION,1)
        self.curl.setopt(self.curl.VERBOSE,0)
        self.curl.setopt(self.curl.HEADER,1)
        self.curl.setopt(self.curl.COOKIELIST,'')
        #self.curl.setopt(self.curl.NOBODY,1)
        try:
            self.curl.perform()
        except pycurl.error as e:
            print('\033[1;31;47m Error: %s.\033[0m\n'%e.args[1])
            sys.exit(2)
        self.reqCount=1
        #self.curl.close()
        body=login_buffer.getvalue()
        if re.search('errorbox',login_buffer.getvalue().decode()):
            print('\033[1;31;47m Error: Failed to Login %s, please check your username/passord.\033[0m\n'%self.zenoss_server)
            sys.exit(1)

    def operate(self,action,method,datalist):
            #self.curl.setopt(self.curl.HTTPHEADER,['Content-Type:application/json,charset=utf-8'])
            self.reqCount +=1
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

            self.reqdata={
                            'type': 'rpc',
                            'data': datalist,
                            'method':method,
                            'action':action,
                            'tid':self.reqCount
                    }
            self.operate_url='http://'+self.zenoss_server+':8080/zport/dmd/'+self.routers[action]+'_router'
            self.curl.setopt(self.curl.POST,1)
            self.curl.setopt(self.curl.URL,self.operate_url)
            #print(urlencode(self.reqdata))
            self.curl.setopt(self.curl.HTTPHEADER,['Content-Type:application/json,charset=utf-8'])
            self.curl.setopt(self.curl.POSTFIELDS,json.dumps(self.reqdata))
            self.curl.setopt(self.curl.HEADER,0)
            operate_buffer=BytesIO()
            self.curl.setopt(self.curl.WRITEDATA,operate_buffer)
            self.curl.perform()
            #print(json.loads(operate_buffer.getvalue().decode()))
            return json.loads(operate_buffer.getvalue().decode())
    def logout(self):
            self.curl.close()

