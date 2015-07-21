#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-07-21 14:32:07

from pyVim.connect import SmartConnect
import requests
import argparse
import getpass
import sys
import ssl

def print_vm_info(virtual_machine, depth=1):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    maxdepth = 10

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(virtual_machine, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = virtual_machine.childEntity
        for c in vmList:
            print_vm_info(c, depth + 1)
        return

    summary = virtual_machine.summary
    annotation = summary.config.annotation

    if summary.guest is not None:
        ip_address = summary.guest.ipAddress
        tools_version = summary.guest.toolsStatus
        powerState=summary.runtime.powerState
        vmname=summary.config.name
        hostname=summary.guest.hostName 
        guest=summary.config.guestFullName
        memsize=str(summary.config.memorySizeMB)
        cpunum=str(summary.config.numCpu)
        if ip_address is not None and powerState=='poweredOn' and 'Red Hat' in guest:
            print(vmname+","+hostname+","+ip_address+","+powerState+","+guest+","+memsize+"MB,"+cpunum+" CPUs")

def main():
    parser= argparse.ArgumentParser()  
    parser.add_argument('-s', '--host',required=True,action='store', help='vSphere service to connect to')

    # because we want -p for password, we use -o for port
    parser.add_argument('-o', '--port',type=int,default=443,action='store',help='Port to connect on')
    parser.add_argument('-u', '--user',required=True,action='store',help='User name to use when connecting to host')
    parser.add_argument('-p', '--password',required=False,action='store',help='Password to use when connecting to host')
    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass(
            prompt='Enter password for host %s and user %s: ' %
                   (args.host, args.user))

    if len(sys.argv) ==1:
        arguments.print_help()
        sys.exit(1)

    default_context = ssl._create_default_https_context
    ssl._create_default_https_context = ssl._create_unverified_context
    requests.packages.urllib3.disable_warnings()

    connection=SmartConnect(host=args.host,user=args.user,pwd=args.password)
    content=connection.RetrieveContent()
    children=content.rootFolder.childEntity

    for child in children:
        if hasattr(child, 'vmFolder'):
            datacenter = child
        else:
            # some other non-datacenter type object
            continue

        vm_folder = datacenter.vmFolder
        vm_list = vm_folder.childEntity
        for virtual_machine in vm_list:
            print_vm_info(virtual_machine, 10)


    return 0

# Start program
if __name__ == "__main__":
    main()
