#!/usr/local/evn python

#autor:mindg.cn
#date:2016.3.3

import ansible.runner
from threading import Thread
import time

print time.ctime() 

def get_info(ip):
    data = []
    runner = ansible.runner.Runner(module_name='setup', module_args='', pattern='all', forks=2)
    datastructure = runner.run()
    sn = datastructure['contacted'][ip]['ansible_facts']['ansible_product_serial']
    sysinfo = datastructure['contacted'][ip]['ansible_facts']['ansible_system']
    cpu = datastructure['contacted'][ip]['ansible_facts']['ansible_processor'][1]
    cpu = ''.join(cpu.split())
    mem = datastructure['contacted'][ip]['ansible_facts']['ansible_memtotal_mb']
    ipadd_pub = datastructure['contacted'][ip]['ansible_facts']['ansible_all_ipv4_addresses'][1]
    ipadd_in = datastructure['contacted'][ip]['ansible_facts']['ansible_all_ipv4_addresses'][0]
    disk = datastructure['contacted'][ip]['ansible_facts']['ansible_devices']['sda']['size']
    data.append((sn,sysinfo,cpu,mem,disk,ipadd_pub,ipadd_in))
    return data

def save_db(data):
    import sqlite3
    conn = sqlite3.connect('info.db')
    cu = conn.cursor()
    sql = '''
         insert into INFO values (?,?,?,?,?,?,?)
         '''
    cu.execute(sql, data[0])
    conn.commit()

def thead_save(i):
    data = get_info(i)
    save_db(data)
if __name__ == '__main__':
    threads = []
    fi = open('hosts', 'r')
    fline = fi.readlines()
    fi.close()
    for i in fline:
        i = i.strip()
        threads.append(Thread(target=thead_save, args=(i,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
