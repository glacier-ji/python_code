#!/usr/bin/env python

#This program is show remote host meminfo
#python version 2.7.9

import os
import argparse
import paramiko


COMMAND = 'free -m'

def show_remote_cpuinfo(hostnmae, port, user, keyfilename):
    sh = paramiko.SSHClient()
    sh.load_system_host_keys()
    #sh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    pkey = keyfilename
    key=paramiko.RSAKey.from_private_key_file(pkey)
    sh.connect(hostname, port, user, pkey=key, timeout=10)

    stdin, stdout,stderr = sh.exec_command(COMMAND)
    result=stdout.read(),stderr.read() 
    if result:
        for line in result:
            print line

    sh.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', action="store", dest="host", default='5.3.1.1')
    parser.add_argument('--port', action="store", dest="port", default=22, type=int)
    parser.add_argument('--user', action="store", dest="user", default="root")
    parser.add_argument('--keyfile', action="store", dest="keyfile", default="/root/.ssh/id_rsa")
    args = parser.parse_args()
    hostname, port, user, keyfilename = args.host, args.port, args.user, args.keyfile
    show_remote_cpuinfo(hostname, port, user, keyfilename)
