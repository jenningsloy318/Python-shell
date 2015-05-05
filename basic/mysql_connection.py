#!/usr/bin/env python3
import mysql.connector
mysql_connection=mysql.connector.connect(user='iterikl',password='synnex2k11',host='Fca-MyGblUat.synnex.org',port='3408',database='onetool')
mysql_cursor = mysql_connection.cursor()
DO_id_sql=("select b.deploy_plan_id,a.cron_do_id,d.server_name,d.domain_name,d.server_ip,e.download_cmd,a.new_version,a.file_path as cvs_file_path,a.operation from itt_cron_do_file a inner join itt_cron_do b on a.cron_do_id = b.id inner join itt_cron_do_runtime c  on b.id = c.cron_do_id inner join itt_cron_server d  on c.cron_server = d.id inner join itt_vcs e on a.vcs_id = e.id where b.deploy_plan_id= %s")
#mysql_cursor.executemany(DO_id_sql,(7183,))
dp=[7183,5684]
dp_tuple=([7183],[5684])
mysql_cursor.execute(DO_id_sql,dp_tuple[1])
#mysql_cursor.executemany(DO_id_sql,dp)
DO_id_result = mysql_cursor.fetchall()
mysql_cursor.close()
for line in DO_id_result:
    print(line,type(line))
mysql_cursor.close()
mysql_connection.close()
  #  ''.join(line)
  #  (deploy_plan_id, cron_do_id, server_name, domain_name, server_ip, download_cmd, new_version, cvs_file_path, operation)=str(line.split(",",9))
  #  print(deploy_plan_id, cron_do_id, server_name, domain_name, server_ip, download_cmd, new_version, cvs_file_path, operation)
