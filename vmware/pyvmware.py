#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-07-21 14:32:07

from __future__ import division
from pyVim.connect import SmartConnect
from pyVmomi import vim
import pyVmomi
import requests
import argparse
import getpass
import sys
import ssl

class pyvmware(object):
    def __init__(self,host,user,passwd):
        self.host=host
        self.user=user
        self.passwd=passwd
    def login(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        default_context = ssl._create_default_https_context
        default_context.verify_mode=ssl.CERT_NONE
        requests.packages.urllib3.disable_warnings()
        self.connection=SmartConnect(host=self.host,user=self.user,pwd=self.passwd)
        return self.connection
    def get_dcs(self):
        self.content=self.connection.RetrieveContent()
        self.viewManager=self.content.viewManager
        self.rootFolder=self.content.rootFolder
        self.dcs=self.viewManager.CreateContainerView(self.rootFolder,[vim.Datacenter],True)
        return self.dcs.view
    def get_datastores(self,datacenter):
        self.datastore=datacenter.datastore
        return self.datastore
        print self.datastore
    def get_clusters(self,datacenter):
        self.hostfolder=datacenter.hostFolder
        clusters=self.hostfolder.childEntity
        return clusters
    def get_top_resourcepool(self,cluster):
        self.top_resourcepool=cluster.resourcePool
        return self.top_resourcepool
    def get_cluster_hosts(self,cluster):
        self.hosts=cluster.host
        return self.hosts
    def get_resourecepool_vms(self,resourcepool,vmlist):
        if  hasattr(resourcepool,'resourcePool') and hasattr(resourcepool,'vm'):
            for vm in resourcepool.vm:
                vmtuple=self.get_vminfo(vm)
                vmlist.append(vmtuple)
            sub_resourcepool=resourcepool.resourcePool
            for c in sub_resourcepool:
                self.get_resourecepool_vms(c,vmlist)
        elif  hasattr(resourcepool,'resourcePool') and not hasattr(resourcepool,'vm'):
            sub_resourcepool=resourcepool.resourcePool
            for c in sub_resourcepool:
                self.get_resourecepool_vms(c,vmlist)
        elif not hasattr(resourcepool,'resourcePool') and  hasattr(resourcepool,'vm'):
            for vm in resourcepool.vm:
                vmtuple=self.get_vminfo(vm)
                vmlist.append(vmtuple)
        return vmlist
    def get_vminfo(self,vm):
        vmsummary=vm.summary
        ip=vmsummary.guest.ipAddress
        vmname=vmsummary.config.name
        hostname=vmsummary.guest.hostName
        guestOS=vmsummary.config.guestFullName
        powerstate=vmsummary.runtime.powerState
        memory=str(vmsummary.config.memorySizeMB)+'MB'
        cpu=(vmsummary.config.numCpu)
        vmtoolstatus=vmsummary.guest.toolsRunningStatus
        vmtoolversion=vmsummary.guest.toolsVersionStatus2
        disks=[]
        for disk in vm.layout.disk:
            diskfile=disk.diskFile[0]
            disks.append(diskfile)
        vminfo=[{'VM name':vmname},{'VM IP address':ip},{'VM Hostname':hostname},{'OS':guestOS},{'Power State':powerstate},{'Memory':memory},{'CPU':cpu},{'VM tool status':vmtoolstatus},{'VM tool Version':vmtoolversion},{'Disks':disks}]
    #    return vmname,ip,hostname,guestOS,powerstate,memory,cpu,vmtoolversion,vmtoolstatus,disks
        return vminfo

    def get_datastore_info(self,datastore):
            datastoresummary=datastore.summary
            freeSpace=datastoresummary.freeSpace
            capability=datastoresummary.capacity
            if freeSpace is not None:
                freeSpace=format(freeSpace/1014/1024/1024,'.0f')
            if capability is not None:
                capability=format(capability/1014/1024/1024,'.0f')
            url=datastore.info.url
            name=datastore.name
            VMs=[]
            for vm in datastore.vm:
                entry=str(vm.name)+':'+str(vm.summary.guest.ipAddress)
                VMs.append(entry)  
            if capability is not None and freeSpace is not None:
                usage='{0:.2%}'.format(1-float(freeSpace)/float(capability),'.4f')
                used=str(usage)+' used'
            elif freeSpace is None:
                used='0%'
            else:
                used='100%'
            datastoreinfo=[{'Datastore Name':name},{'Used':used},{'Total Space':str(capability)+'G'},{'Free Space':str(freeSpace)+'G'},{'VM List':VMs}]
    #        return 'Datastore Name: '+str(name),'Datastore Location: '+str(url),'Used: '+str(used),'Total Space: '+str(capability)+'G','Free Space: '+str(freeSpace)+'G',VMs
            return datastoreinfo

