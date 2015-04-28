These are practice of python learning for system adminitrators
multi-process-checking_per_server.py is used for login to multiple serves at same time to do same operations, its has parallel running multiple ssh sessions, the log is ordered by server .
multi-process-checking.py is used as the same purpose, just all logs are mixed 
        usage: multi-processes-checking_per_server.py [-h] [-s [SERVER_LIST]] [-l [LOG]] [-c [CMD_LIST]] [-l [LOG]]
        usage:  multi-processes-checking.py [-h] [-s [SERVER_LIST]] [-c [CMD_LIST]] [-l [LOG]] [-c [CMD_LIST]] [-l [LOG]]
        
        optional arguments:
          -h, --help            show this help message and exit
          -s [SERVER_LIST], --server_list [SERVER_LIST]
                                The servers list
          -c [CMD_LIST], --cmd_list [CMD_LIST]
                                The command list
          -l [LOG], --log [LOG]
                                The log file,default result.log
single-process-checking.py only run one ssh session at a time.usage is same as previous ones.
