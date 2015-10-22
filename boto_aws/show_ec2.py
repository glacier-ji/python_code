#!/usr/bin/env python

#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import os
import smtplib
from email.MIMEText import MIMEText  
from email.mime.multipart import MIMEMultipart
import boto
from boto import ec2

def getAllInstances():
    instances=[]
    conn=ec2.connect_to_region('cn-north-1')
    for instance in conn.get_only_instances():
        ins={}
        ins['instance_id']=instance.id
        ins['name']=instance.tags.get('Name','').encode('gb2312')
        ins['project']=instance.tags.get('PROJECT','')
        ins['instance_type']=instance.instance_type
        ins['state']=instance.state
        ins['placement']=instance.placement
        ins['private_ip']=instance.private_ip_address
        ins['public_ip']=instance.ip_address
        ins['vpc_id']=instance.vpc_id
        ins['subnet_id']=instance.subnet_id
        ins['image_id']=instance.image_id
        ins['virtualization_type']=instance.virtualization_type
        ins['launch_time']=instance.launch_time
        instances.append(ins)
    return instances

def send_mail(filename):
    msg = MIMEMultipart()
    fp = open(filename, 'rb')
    text = fp.read()
    fp.close()
    info = MIMEText(text,_subtype="plain",_charset="gb2312")
    msg.attach(info)
    #create attachement 
    att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="ins.csv"'
    msg.attach(att1) 
    #add mail header
    msg['Subject'] = 'This is all taiwan instances'
    msg['To'] = ''
    msg['From'] = 'mail address'
    try:
        smtp = smtplib.SMTP('smtp@server.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo
        smtp.login('mail address', '')
        #smtp.set_debuglevel(1)
        smtp.sendmail('sender mail address', ['mail1','mail2'],msg.as_string())
    except Exception, e:
        print 'Error: %s' %str(e)
    finally:
        smtp.close()
if __name__ == '__main__':
    import csv
    f = open('ins.csv', 'wt')
    instances = getAllInstances()
    info = []
    for key in instances[0].keys():
        info.append(key)
    info = sorted(info)
    headers = dict((n,n) for n in info)
    dict_writer = csv.DictWriter(f, fieldnames = sorted(instances[0].keys()))
    dict_writer.writerow(headers)
    dict_writer.writerows(instances)
    f.close()
    send_mail('ins.csv')
