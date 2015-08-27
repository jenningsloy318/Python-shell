#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-08-26 09:08:38
# import objects and constants
from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL
import sys
import re
import argparse
import getpass
def ldapaccts(servername,ldappw):
        ldapacct_list=[]
        ldapserver='ldap://10.88.126.150'
        dn='cn=root,dc=synnex,dc=org'
        ldap_base='ou='+servername+',ou=proftpd servers,dc=synnex,dc=org'
        # define the Server and the Connection objects
        ldapserver='ldap://10.88.126.150'
        #s = Server(ldapserver, port = 389, get_info = ALL)  # define an unsecure LDAP server, requesting info on the server and the schema
        #c = Connection(s, auto_bind = True, client_strategy = SYNC, user=dn, password=pw, authentication=SIMPLE, check_names=True)
        ldapconn=Connection(ldapserver,auto_bind=True,client_strategy = SYNC, user=dn, password=ldappw, authentication=SIMPLE, check_names=True)
        #print(s.info) # display info from the server. OID are decoded when recognized by the library
        #c.search(search_base=ldap_base,search_filter='')
        entry_list = ldapconn.extend.standard.paged_search(search_base =ldap_base,
                                                    search_filter='(objectClass=shadowAccount)',
                                                    search_scope=SUBTREE,
                                                    attributes=['uid'],
                                                    paged_size=5,
                                                    generator=False)
        for entry in entry_list:
            user=''.join(entry['attributes']['uid'])
            ldapacct_list.append(user)
            #print(user)
            #print(entry['attributes']['uid'])
        # request a few objects from the LDAP server
        ldapconn.unbind()
        return ldapacct_list
        
def analyze(authfile):
    username_logintime={}
    login_pattern = re.compile(r'"USER\s+\w+"')
    for loginline in open(authfile):
        if login_pattern.search(loginline):
            loginline_list=loginline.split()
            if loginline.startswith('Synnex'):
                username=loginline_list[8].replace('"','')
                logintime=loginline_list[5].replace('[','')
            else:
                username = loginline_list[7].replace('"', '')
                logintime = loginline_list[4].replace('[', '') 
            username_logintime[username] = logintime
    return username_logintime

if __name__ == '__main__':
        arguments = argparse.ArgumentParser()  
        arguments.add_argument("-s","--server",nargs="?",help="The servers name")
        arguments.add_argument("-i","--inputauthfile", nargs="?",help="The input ftp auth file")
        arguments.add_argument("-on","--onologin", nargs="?",help="output of no login")
        arguments.add_argument("-ol","--ologin", nargs="?",help="output of login")
        if len(sys.argv) ==1:
            arguments.print_help()
            sys.exit(1)
        args = arguments.parse_args()
        server=args.server
        authinfile=args.inputauthfile
        nologin_outfile=open(args.onologin,'w')
        login_outputfile=open(args.ologin,'w')
        passwd=getpass.getpass('The ldap passwd:')
        ldapacctslist=ldapaccts(server,passwd)
        logintime_dict=analyze(authinfile)
        for acct in ldapacctslist:
            if acct in logintime_dict.keys():
                print(server,acct,logintime_dict[acct])
                login_outputfile.write(server+','+acct+','+logintime_dict[acct]+'\n')
            else:
                print(server,acct,'0')
                nologin_outfile.write(server+','+acct+',0\n')
        nologin_outfile.close()
        login_outputfile.close()
