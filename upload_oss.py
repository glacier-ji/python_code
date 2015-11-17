#!/usr/bin/python env
#autor:glacier
#date:2015-11-16
 
import os,os.path,time
import operator
import time
from oss.oss_api import *
 
prefix = '/home/dbback'
logtime = time.strftime(time.ctime())
#filelist = [ file for file in os.listdir(os.path.dirname(os.path.abspath(__file__))) if os.path.isfile(file) ]
filelist = [ file for file in os.listdir(prefix) if os.path.isfile(prefix + '/' + file) ] 
 
 
def get_time(filename):
    ft = os.stat(filename)
    return ft.st_ctime
 
#def get_max():
#    flist = []
#    for file in filelist:
#        flist.append(os.stat(file).st_ctime)
#    return max(flist)
 
def get_dist():
    d = {}
    for file in filelist:
        d[file] = get_time(prefix + '/' + file)
    return d
   
if __name__ == '__main__':
    #maxtime = get_max()
    d = get_dist()
    #dic= sorted(d.iteritems(), key=lambda d:d[1], reverse = True)
    upfile = max(d.iteritems(), key=operator.itemgetter(1))[0]
    endpoint = "your aliyun endpoint"
    accessKeyId, accessKeySecret="your accessKeyId","your accessKeySecret "
    oss = OssAPI(endpoint, accessKeyId, accessKeySecret)
    res = oss.put_object_from_file("bucketname",upfile,prefix + '/' + upfile)
    if res.status != 200:
        with open('/var/log/dbback.log', 'a+') as f:
            f.write(logtime + ' back failed' + '\n')
