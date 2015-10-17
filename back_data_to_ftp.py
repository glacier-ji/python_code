#coding=utf-8

import time
import os.path
import re
import ConfigParser
from ftplib import FTP
import subprocess
from subprocess import Popen,PIPE

cf = ConfigParser.ConfigParser()
cf.read('cfg.ini')
ftp_server = cf.get('server', 'address')
ftp_port = cf.get('server', 'port')
username = cf.get('user', 'user')
password = cf.get('user', 'password')
cmd_path = cf.get('winrar_path', 'rar_path')
cmd_rar = 'rar a -r '
back_target = cf.get('upload', 'back_target')
#save_path = cf.get('upload', 'save_path')
#str_cmd = 'C:\\"Program Files"\\WinRAR\\rar.exe a -r' + ' e:\\webadmin' + time.strftime('%Y%m%d%H%M%S') + '.rar' + ' e:\\webadmin'
str_cmd = cmd_path + cmd_rar + back_target + time.strftime('%Y%m%d%H') +  '.rar ' + back_target
pattern = '100%'

def rar_file():
    p = subprocess.Popen(str_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout,stderror=p.communicate()
    match = re.search(pattern, stdout)
    if  match.start():
        return 'ok'

def ftp_conn():
    ftp = FTP()
    ftp.connect(ftp_server, ftp_port)
    return  ftp

def ftp_upload():
    ftp = ftp_conn()
    ftp.login(username,password)
    remotepath = os.path.basename(back_target) + time.strftime('%Y%m%d%H') + '.rar'
    bufsize = 1024
    localpath = os.path.dirname(back_target) + '\\'+ os.path.basename(back_target) + time.strftime('%Y%m%d%H') + '.rar'
    fp = open(localpath,'rb')
    ftp.storbinary('STOR '+ remotepath ,fp,bufsize)
    fp.close()
    ftp.quit()

# def ftp_download():
#     ftp = ftp_conn()
#     ftp.set_debuglevel(2)
#     ftp.connect(ftp_server,2258)
#     ftp.login(username,password)
#     #ftp.set_pasv(1)
#     remotepath =r'/MyIPSec.ipsec'
#     bufsize = 1024
#     localpath =r'e:\i\MyIPSec.ipsec'
#     fp = open(localpath,'wb')
#     ftp.retrbinary('RETR '+ remotepath ,fp.write,bufsize)
#     fp.close()
#     ftp.quit()

if __name__ == '__main__':
    status = rar_file()
    if status == 'ok':
        ftp_upload()


