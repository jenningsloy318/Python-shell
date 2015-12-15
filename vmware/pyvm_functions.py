#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-07-21 14:32:07

from pyVim.connect import SmartConnect
from pyVmomi import vim
import pyVmomi
import requests
import argparse
import getpass
import sys
import ssl

if __name__ == "__main__":
    #parser= argparse.ArgumentParser()  
    #parser.add_argument('-s', '--host',required=True,action='store', help='vSphere service to connect to')

    ## because we want -p for password, we use -o for port
    #parser.add_argument('-o', '--port',type=int,default=443,action='store',help='Port to connect on')
    #parser.add_argument('-u', '--user',required=True,action='store',help='User name to use when connecting to host')
    #parser.add_argument('-p', '--password',required=False,action='store',help='Password to use when connecting to host')
    #args = parser.parse_args()

    #if not args.password:
    #    args.password = getpass.getpass(
    #        prompt='Enter password for host %s and user %s: ' %
    #               (args.host, args.user))

    #if len(sys.argv) ==1:
    #    arguments.print_help()
    #    sys.exit(1)

    #default_context = ssl._create_default_https_context
    #ssl._create_default_https_context = ssl._create_unverified_context
    #requests.packages.urllib3.disable_warnings()

    #connection=SmartConnect(host=args.host,user=args.user,pwd=args.password)
    try:
        default_context = ssl._create_default_https_context
        default_context.verify_mode=ssl.CERT_NONE
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings()
        connection=SmartConnect(host='fca-vc8',user='jenningsl@synnexorg',pwd='synnex-2013')
        content=connection.RetrieveContent()
        viewManager=content.viewManager
        inventory=viewManager.CreateInventoryView()
        rootFolder=content.rootFolder

        #ResourcePools=viewManager.CreateContainerView(rootFolder,[vim.ResourcePool],True)
        #for obj in ResourcePools.view:
        #    print('ResourcePool:',obj.name,obj)


        Clusters=viewManager.CreateContainerView(rootFolder,[vim.ComputeResource],True)
        for cluster in Clusters.view:
            print('Cluster:',cluster.name,cluster)
            resourcePoolroot=cluster.resourcePool
            ResourcePools=resourcePoolroot.resourcePool
            hosts=cluster.host
            #print('resourcePoolroot:',resourcePoolroot.name,resourcePoolroot)
            #print('ResourcePools:',ResourcePools)
            #print('Hosts:',hosts)
        for rp in ResourcePools:
            print(rp.name,rp)



        rootFolderChildren=content.rootFolder.childEntity
        for child in rootFolderChildren:
            if hasattr(child,'vmFolder'):
                datacenter=child
            else:
                continue
        print('Datecenter:',datacenter.name,datacenter)
        hostFolder=datacenter.hostFolder
        print('hostFolder:',hostFolder.name,hostFolder)

        vmfolder=datacenter.vmFolder
    except vim.fault.InvalidLogin:
        print('Invalid user or passsword')
    except requests.exceptions.ConnectionError:
        print('Can\'t connect to the vcenter server')
    
    #print(vmfolder.childEntity)

    

