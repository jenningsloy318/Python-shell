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
    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        default_context = ssl._create_default_https_context
        default_context.verify_mode=ssl.CERT_NONE
        requests.packages.urllib3.disable_warnings()

    def login(self,host,user,passwd):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.connection=SmartConnect(host=self.host,user=self.user,pwd=self.passwd)
        self.content=self.connection.RetrieveContent()
        self.viewManager=self.content.viewManager
        self.rootFolder=self.content.rootFolder
        self.dcs=self.viewManager.CreateContainerView(self.rootFolder,[vim.Datacenter],True).view[0]

    def get_dcs(self):
        dcs={}
        dcs[self.dcs.name]=self.dcs
        return dcs

    def get_datastores(self):
        datastores={}
        self.datastores=self.dcs.datastore
        for datastore in self.datastores:
            datastores[datastore.name]=datastore
        return datastores

    def get_clusters(self):
        clusters={}
        self.hostfolder=self.dcs.hostFolder
        self.clusters=self.hostfolder.childEntity
        for cluster in self.clusters:
            clusters[cluster.name]=cluster
        return clusters

    def get_cluster_top_resourcepool(self,cluster):
        cluster_top_resourcepools={}
        cluster_top_resourcepools[cluster.name]=cluster.resourcePool
        return cluster_top_resourcepools

    def get_all_top_resourcepools(self):
        all_top_resourcepools={}
        for cluster in self.get_clusters().values():
            all_top_resourcepools[cluster.name]=cluster.resourcePool
        return all_top_resourcepools

    def get_sub_resourcepools(self,resourcepool):
        sub_resourcepools={}
        for sub_resourcepool in resourcepool.resourcePool:
            sub_resourcepools[sub_resourcepool.name]=sub_resourcepool
        return sub_resourcepools

    def get_cluster_hosts(self,cluster):
        cluster_hosts={}
        self.hosts=cluster.host
        for host in self.hosts:
            cluster_hosts[host.name]=host
        return cluster_hosts

    def get_all_hosts(self):
        all_hosts={}
        for cluster in self.get_clusters().values():
            for host in cluster.host:
                all_hosts[host.name]=host
        return all_hosts
        

    def get_all_vms(self,vmdict):
        for top_resourcepool in self.get_all_top_resourcepools().values():
            self.get_resourecepool_vms(top_resourcepool,vmdict)

    def get_cluster_vms(self,cluster,vmdict):
        top_resourcepool=self.get_cluster_top_resourcepool(cluster).values()
        self.get_resourecepool_vms(top_resourcepool,vmdict)

    def get_resourecepool_vms(self,resourcepool,vmdict):
        if  hasattr(resourcepool,'resourcePool') and hasattr(resourcepool,'vm'):
            for vm in resourcepool.vm:
                vmdict[vm.name]=vm
            sub_resourcepool=resourcepool.resourcePool
            for c in sub_resourcepool:
                self.get_resourecepool_vms(c,vmdict)
        elif  hasattr(resourcepool,'resourcePool') and not hasattr(resourcepool,'vm'):
            sub_resourcepool=resourcepool.resourcePool
            for c in sub_resourcepool:
                self.get_resourecepool_vms(c,vmdict)
        elif not hasattr(resourcepool,'resourcePool') and  hasattr(resourcepool,'vm'):
            for vm in resourcepool.vm:
                vmdict[vm.name]=vm

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
        vminfo={'vmName':vmname,'vmIP':ip,'vmHostname':hostname,'vmOS':guestOS,'vmPowerState':powerstate,
                'vmMemory':memory,'vmCPU':cpu,'vmtoolStatus':vmtoolstatus,'vmToolVersion':vmtoolversion,'vmDisks':disks}
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
            datastoreinfo=[{'DatastoreName':name},{'Used':used},{'TotalSpace':str(capability)+'G'},{'FreeSpace':str(freeSpace)+'G'},{'vmList':VMs}]
            return datastoreinfo

