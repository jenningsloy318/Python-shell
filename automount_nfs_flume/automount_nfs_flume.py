#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Jennings Liu@ 2016-10-10 15:09:09

import socket
import fcntl
import struct
import re
import subprocess
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

All_server_mount={'cron2.synnex.org':'/mnt/uscron2_spool','cron3.synnex.org':'/mnt/uscron3_spool','cron1.hyvesolutions.org':'/mnt/hycron1_spool','gis.synnex.org':'/mnt/edigis_spool','fca-vm-prod-esearch-index.synnex.org':'/mnt/esearch_spool','mxcron.synnex.org':'/mnt/mxcron_spool','cacron1.synnex.org':'/mnt/cacron1_spool','cron1-uk.synnex.org':'/mnt/ukcron1_spool','caedi.synnex.org':'/mnt/caedi_spool'}

# regex expression to determine pattern
LocalNet=('.').join(get_ip_address('eth0').split('.')[:2])
if LocalNet=='10.88':
    pattern=re.compile(r'10.88')
elif LocalNet=='10.84':
    pattern=re.compile(r'10.84|10.93|192.168.18')
else:
    pattern=re.compile('')
##modify the dictionary according to the pattern
for host in All_server_mount.keys():
    #hostIP=socket.gethostbyname_ex(host)[2][0]
    hostIP=socket.gethostbyname(host)
    if not pattern.search(hostIP):
        All_server_mount.pop(host)

## umount and remount the nfs

for server in All_server_mount.keys():
    print('Umounting '+All_server_mount[server]+'!') 
#    print('umount -l '+All_server_mount[server])
    umount_out=subprocess.Popen('umount -l '+All_server_mount[server],shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    if not umount_out[1]:
    	print('Umount successfully '+All_server_mount[server]+umount_out[0]+'!') 
    	print('Re-mounting the nfs share!')
    	print('mount '+server+':/logs/flume '+All_server_mount[server])
    	mount_out=subprocess.Popen('mount '+server+':/logs/flume '+All_server_mount[server],shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    	if not mount_out[1]:
    		print('Mount successfully '+mount_out[0]+'!\n') 
    	else:
    		print("Mount failed "+mount_out[0],mount_out[1],'!\n') 
    else:
	print("Umount "+All_server_mount[server]+" Failed, so will not re-mount it again!\n")




df_out=subprocess.Popen('df -h',shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
for df_line in df_out:
	print(df_line)
