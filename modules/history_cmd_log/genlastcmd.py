#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-06-26 17:12:44


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class cmdgen(object):
    def __init__(self, type):
        self.type=type
    def cmdout(self):
         import os
         import paramiko
         import sys
         from multiprocessing import Pool
         from multiprocessing.dummy import Pool as ThreadPool
         import argparse
         import time
         import datetime
         import socket
         from dateutil.relativedelta import relativedelta
         current_time=datetime.datetime.now()
         monthdelta=relativedelta(months=-1)
         yeardelta=relativedelta(years=-1)
         time_1_month_ago=current_time+monthdelta
         time_2_month_ago=time_1_month_ago+monthdelta
         time_3_month_ago=time_2_month_ago+monthdelta
         time_4_month_ago=time_3_month_ago+monthdelta
         time_5_month_ago=time_4_month_ago+monthdelta
         time_6_month_ago=time_4_month_ago+monthdelta
         last_year=current_time+yeardelta
         grep_month=time_1_month_ago.strftime('%Y-%b')+'|'+time_2_month_ago.strftime('%Y-%b')+'|'+time_3_month_ago.strftime('%Y-%b')+'|'+time_4_month_ago.strftime('%Y-%b')+'|'+time_5_month_ago.strftime('%Y-%b')+'|'+time_6_month_ago.strftime('%Y-%b')
         grep_year=current_time.strftime('%Y')+'|'+last_year.strftime('%Y')
         if self.type=='linux':
            lastlog_summary_title='echo "Server_IP,Hostname,Acct,Number of Acct access,Type"'
            lastlog_summary='''last -F -w |grep -E -v "down|eboot"|grep -E "'''+grep_year+'''"|awk '{print $1,$8"-"$5}'|grep -E "'''+grep_month+'''"|sort -k1|awk '{print $1}'|uniq -c|awk -v HOSTNAME=`hostname` -v local_accts="`getent --service=files passwd | awk -F: '{print$1}'`"  '{if(local_accts~$2){print HOSTNAME","$2","$1",Local";}else{print HOSTNAME","$2","$1",LDAP";}}' '''
            accts_in_lastlog_summary='''login_accts=`last -F -w |grep -E -v "down|eboot"|grep -E "'''+grep_year+'''"|awk '{print $1,$8"-"$5}'|grep -E "'''+grep_month+'''"|sort -k1|awk '{print $1}'|uniq -c|awk '{print $2}'` '''
            accts_of_local_non_access=accts_in_lastlog_summary+''';for acct in `getent --service=files passwd| egrep -v "abrt|nfsnobody|saslauth|rabbitmq|mysql|nrpe|clam|memcached|rrdcached|nagios|redis|ntop|vpn|zenoss|dovenull|mapred|zookeeper|impala|noaccess|nobody|ftp|ssh|avahi|false|nologin"|awk -F: '{ if ( $3 > 100 ) print  $1}'`;do echo $login_accts|grep -q $acct;[ $? -ne 0 ] && echo "$HOSTNAME,$acct,0,Local" ; done'''
            accts_of_ldap_non_access=accts_in_lastlog_summary+''';for acct in `getent --service=ldap passwd| egrep -v "abrt|nfsnobody|saslauth|rabbitmq|mysql|nrpe|clam|memcached|rrdcached|nagios|redis|ntop|vpn|zenoss|dovenull|mapred|zookeeper|impala|noaccess|nobody|ftp|ssh|avahi|false|nologin"|awk -F: '{ if ( $3 > 100 ) print  $1}'`;do echo $login_accts|grep -q $acct;[ $? -ne 0 ] && echo "$HOSTNAME,$acct,0,LDAP" ; done'''
         elif self.type=='solaris':
            lastlog_summary_title='echo "Server_IP,Hostname,Acct,Number of Acct access,Type"'
            lastlog_summary='''local_accts="`cat /etc/passwd |grep -v "^#"| /usr/xpg4/bin/awk -F: '{print $1}'`";cat /var/adm/wtmpx | /usr/lib/acct/fwtmp|/usr/xpg4/bin/grep -E "pts|console"|/usr/xpg4/bin/grep -E -v "login|telnet|down|eboot|LOGIN"|/usr/xpg4/bin/grep -E "'''+grep_year+'''"| /usr/xpg4/bin/awk '{print $1,$NF"-"$(NF-3)}'|/usr/xpg4/bin/grep -E "'''+grep_month+'''"|sort -k1| /usr/xpg4/bin/awk '{print $1}'|uniq -c| /usr/xpg4/bin/awk '{print $0}'| while read line; do  acct=`echo $line| awk '{print $2}'` ;[[ "$local_accts" =~ "$acct" ]] && echo $line |/usr/xpg4/bin/awk -v HOSTNAME=`hostname` '{print HOSTNAME","$2","$1",Local"}' || echo $line |/usr/xpg4/bin/awk -v HOSTNAME=`hostname` '{print HOSTNAME","$2","$1",LDAP"}' ;done'''
            accts_in_lastlog_summary='''login_accts=`cat /var/adm/wtmpx | /usr/lib/acct/fwtmp|/usr/xpg4/bin/grep -E "pts|console"|/usr/xpg4/bin/grep -E -v "login|telnet|down|eboot|LOGIN"|/usr/xpg4/bin/grep -E "'''+grep_year+'''"|awk '{print $1,$NF"-"$(NF-3)}'|/usr/xpg4/bin/grep -E "'''+grep_month+'''"|sort -k1|awk '{print $1}'|uniq -c|awk '{print $2}'` '''
            accts_of_local_non_access=accts_in_lastlog_summary+''';for acct in `cat /etc/passwd|grep -v "^$"| egrep -v "abrt|nfsnobody|saslauth|rabbitmq|mysql|nrpe|clam|memcached|rrdcached|nagios|redis|ntop|vpn|zenoss|dovenull|mapred|zookeeper|impala|noaccess|nobody|ftp|ssh|avahi"|awk -F: '{ if ( $3 > 100 ) print  $1}'`;do echo $login_accts|/usr/xpg4/bin/grep -q $acct;[ $? -ne 0 ] && echo "$HOSTNAME,$acct,0,Local" ; done'''
            accts_of_ldap_non_access=accts_in_lastlog_summary+''';for acct in `ldaplist passwd | awk -F, '{print $1}' | awk -F"=" '{print$2}' |grep -v "^$"`;do echo $login_accts|/usr/xpg4/bin/grep -q $acct;[ $? -ne 0 ] && echo "$HOSTNAME,$acct,0,LDAP" ; done'''
         return lastlog_summary_title,lastlog_summary,accts_of_local_non_access,accts_of_ldap_non_access 
