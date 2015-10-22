#!/usr/bin/evn python

import boto
from boto import ec2
import time

region = 'cn-north-1'

def create_volume(volume_size, device_name):
    ec2 = ec2 = boto.ec2.connect_to_region(region)
    azone = ec2.get_only_instances()[0].placement
    volume = ec2.create_volume(volume_size, azone)
    while volume.status != 'available':
        print '#'
        time.sleep(5)
        volume.update()
    instance_id = ec2.get_only_instances()[0].id 
    if instance_id == u'i-6b46fc53':
        volume.attach(instance_id, device_name)


create_volume(10, '/dev/xvdb')
