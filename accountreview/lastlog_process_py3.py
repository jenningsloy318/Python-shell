#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-08-26 16:53:08

import re
import argparse
import sys
import subprocess
import platform
year1='2015'
year2='2014'
loginsummary={}

arguments = argparse.ArgumentParser()  
arguments.add_argument("-p","--passwdfile",nargs="?",help="the passwd file",default='/etc/passwd')
arguments.add_argument("-o","--output",nargs="?",help="the output file",required=True)
if len(sys.argv) ==1:
    arguments.print_help()
    sys.exit(1)
args = arguments.parse_args()
passwdfile=args.passwdfile
outfile=open(args.output,'w')

if platform.system() == 'Linux':
    last_command='last -F'
else:
    last_command='cat /var/adm/wtmpx | /usr/lib/acct/fwtmp'

lastlog=subprocess.Popen(last_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate() 
osname=bytes.decode(subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]).rstrip()

for acctline1 in open(passwdfile):      # initial the loginsummary dict
        acct=acctline1.split(':')[0]
        acctnum=acctline1.split(':')[2]
        pattern0=re.compile(r'^no|sshd|system|nfs')
        if (int(acctnum)==0 or int(acctnum)>100) and not pattern0.search(acct):
                loginsummary[acct]=0

for  lastline in lastlog[:]:          # analyze the login times

    for key in loginsummary.keys():
        pattern1=re.compile(r'%s'% key)
        pattern2=re.compile(r'%s' % (year1))
        if pattern1.search(str(lastline)) and pattern2.search(str(lastline)):
            loginsummary[key]=loginsummary[key]+1

for key in loginsummary.keys():         #print the acct and its login times
    outfile.write(osname+','+key+','+str(loginsummary[key])+'\n')
    print(osname,key,loginsummary[key])
outfile.close()
