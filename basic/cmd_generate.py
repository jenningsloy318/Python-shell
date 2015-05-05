#!/usr/bin/env python3
import datetime
from dateutil.relativedelta import relativedelta
def main():
    global cmd_list
    current_time=datetime.datetime.now()
    monthdelta=relativedelta(months=-1)
    #monthdelta=datetime.timedelta(days=-30)
    #yeardelta=datetime.timedelta(days=-365)
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
    cmd_lastlog='cat /var/adm/wtmpx | /usr/lib/acct/fwtmp'+'|'+'/usr/xpg4/bin/grep -E "pts|console"|'+'/usr/xpg4/bin/grep -E -v "login|telnet|down|eboot|LOGIN"'+'|'+'/usr/xpg4/bin/grep -E "'+grep_year+'"'+'|'+'awk '''''{print $1,$NF"-"$(NF-3)}'''+"'"+'|/usr/xpg4/bin/grep -E "'+grep_month+'"'+'|sort -k1|'+'awk '''''{print $1}'''+"'"+'|uniq -c|'+'awk '''''{print $2":"$1}'''+"'"
    cmd_lastlog_accts='login_accts=`cat /var/adm/wtmpx | /usr/lib/acct/fwtmp'+'|'+'/usr/xpg4/bin/grep -E "pts|console"|'+'/usr/xpg4/bin/grep -E -v "login|telnet|down|eboot|LOGIN"'+'|'+'/usr/xpg4/bin/grep -E "'+grep_year+'"'+'|'+'awk '''''{print $1,$NF"-"$(NF-3)}'''+"'"+'|/usr/xpg4/bin/grep -E "'+grep_month+'"'+'|sort -k1|'+'awk '''''{print $1}'''+"'"+'|uniq -c|'+'awk '''''{print $2}'''+"'`"
    cmd_lastlog_title='echo "Server_IP:   Acct:  Number of Acct access"'
    cmd_non_OS_acct='cat /etc/passwd| egrep -v "abrt|nfsnobody|saslauth|rabbitmq|mysql|nrpe|clam|memcached|rrdcached|nagios|redis|ntop|vpn|zenoss|dovenull|mapred|zookeeper|impala|noaccess|nobody|ftp|ssh|avahi" |'+'awk -F: '''''{ if ( $3 > 100 ) print  $1}'''+"'"
    cmd_non_OS_acct_title='echo "Server_IP:   Non OS accts"'
    cmd_non_access=cmd_lastlog_accts+';for acct in `cat /etc/passwd| egrep -v "abrt|nfsnobody|saslauth|rabbitmq|mysql|nrpe|clam|memcached|rrdcached|nagios|redis|ntop|vpn|zenoss|dovenull|mapred|zookeeper|impala|noaccess|nobody|ftp|ssh|avahi"'+'|awk -F: '''''{ if ( $3 > 100 ) print  $1}'''+"'`;"+'do echo $login_accts|/usr/xpg4/bin/grep -q $acct;[ $? -ne 0 ] && echo "$acct" ; done'
    cmd_non_access_title='echo "Server_IP:   Non-Access Accouts "'
    cmd_list=[cmd_non_OS_acct_title,cmd_non_OS_acct,cmd_lastlog_title,cmd_lastlog,cmd_non_access_title,cmd_non_access]

    for cmd in cmd_list:
        if 'Server_IP' in cmd:
            print(cmd)
        else:
            print('abc')
if __name__ == "__main__":
    main()
