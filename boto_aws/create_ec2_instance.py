#!/usr/bin/env python

import os
import time
import boto
from boto import ec2


def launch_instance(ami='ami-a8e87591',
                    instance_type='t2.micro',
                    key_name='pro',
                    key_extension='.pem',
                    key_dir='~/.ssh',
                    group_name='bicher',
                    ssh_port=22,
                    cidr='0.0.0.0/0',
                    tag='pow',
                    user_data=None):

    ec2 = boto.ec2.connect_to_region('cn-north-1')
    try:
        key = ec2.get_all_key_pairs(keynames=[key_name])[0]
    except ec2.ResponseError, e:
        if e.code == 'InvalidKeyPair.NotFound':
            print 'Creating keypair: %s' % key_name
            key = ec2.create_key_pair(key_name)
            key.save(key_dir)
        else:
            raise
    try:
        group = ec2.get_all_security_groups(groupnames=[group_name])[0]
    except ec2.ResponseError, e:
        if e.code == 'InvalidGroup.NotFound':
            print 'Creating secuity group:%s' % group_name
            group = ec2.create_security_group(group_name, 'A group that all ssh access')
        else:
           raise
    try:
        group.authorize('tcp', ssh_port, ssh_port, cidr)
    except ec2.ResponseError, e:
        if e.code == 'InvalidPermission.Duplicate':
            print 'security group: %s already authorized' % group_name
        else:
            raise

    reservation = ec2.run_instances(ami, key_name=key_name, security_groups=[group_name], instance_type=instance_type, user_data=user_data)
    instance = reservation.instances[0]

    print 'waiting for  instance'
    while instance.state != 'running':
        print '.'
        time.sleep(5)
        instance.update()
    print 'done'

    instance.add_tag(tag)


    return instance

user_data ="echo \"I am runing when instance start\" | tee /root/process_start.txt"


launch_instance(ami='ami-a8e87591',\
                instance_type='t2.micro',\
                key_name='test20150513',\
                key_extension='.pem',\
                key_dir='~/.ssh',\
                group_name='control-cc',\
                ssh_port=22,\
                cidr='0.0.0.0/0',\
                tag='pro',\
                user_data=user_data)

