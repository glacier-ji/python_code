#encoding=utf-8
#__author__ = 'glacier'
#date:20151025

import os.path
import ConfigParser
from ftplib import FTP_TLS
from threading import Thread
import socket
import ssl

cf = ConfigParser.ConfigParser()
cf.read(r'e:\project1\ftplist.txt')

user = 'check_login'
password = '45H'
server_info = []

#定义FTP_TLS类
class IMPLICIT_FTP_TLS(FTP_TLS):
    def __init__(self, host='', user='', passwd='', acct='', keyfile=None,
        certfile=None, timeout=60):
        FTP_TLS.__init__(self, host, user, passwd, acct, keyfile, certfile, timeout)

    def connect(self, host='', port=0, timeout=-1):
        if host != '':
            self.host = host
        if port > 0:
            self.port = port
        if timeout != -1:
            self.timeout = timeout
        try:
            self.sock = socket.create_connection((self.host, self.port), self.timeout)
            #self.af = self.sock.family
            self.sock = ssl.wrap_socket(self.sock, self.keyfile, self.certfile)
            self.file = self.sock.makefile('rb')
            self.welcome = self.file.readline()
        except Exception as e:
            print e
        return self.welcome


#获得配置文件信息，转换成列表
def get_ip_port():
    for arg in cf.sections():
        ip, port = cf.options(arg)
        ip = cf.get(arg, ip)
        port = cf.get(arg, port)
        info = (ip, port)
        server_info.append(info)
    return server_info

#检查函数，测试是否ftp登录ok
def check_login(ftp_server, ftp_port):
    try:
        ftps = IMPLICIT_FTP_TLS()
        #print help(ftps)
        ftps.connect(host=ftp_server, port=ftp_port)
        ftps.login(user=user, passwd=password)
        ftps.quit()
        return 1
    except:
        return 0

#根据检查的成功或失败，写入文件
def write_status(ftp_server, ftp_port):
    result = check_login(ftp_server, ftp_port)
    f = open(r'e:\project1\status.txt', 'a+')
    if result == 1:
        f.write(ftp_server + ' login ok' + '\n')
    else:
        f.write(ftp_server + ' login error' + '\n')
    f.close()

#主函数，判断文件大小是否为0，非0重置文件，保持文件内容最新，多线程检查。
if __name__ == '__main__':
    threads = []
    server_info = get_ip_port()
    if os.path.getsize(r'e:\project1\status.txt'):
        f = open(r'e:\project1\status.txt', 'r+')
        f.truncate()
        f.close()
    for i in range(0, len(cf.sections())):
        ip, port = server_info[i]
        threads.append(Thread(target=write_status, args=(ip, port)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

