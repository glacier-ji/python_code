#!/usr/bin/env python

import boto
from boto import ec2

region = 'cn-north-1'

def allocate_ip():
    ec2 = boto.ec2.connect_to_region(region)
    address = ec2.allocate_address(domain='vpc',dry_run=False)
    return address.public_ip,address.allocation_id

def eip_associate(instanceid):
    ec2 = boto.ec2.connect_to_region(region)
    address = ec2.get_all_addresses(addresses='5.2.29.7')
    ec2.associate_address(instanceid,address[0].public_ip)


#eip_associate('i-6b46fc53')

def dis_eip_associate(public_ip):
    ec2 = boto.ec2.connect_to_region(region)
    address = ec2.get_all_addresses(addresses='5.2.29.7')
    association_id = address[0].association_id
    ec2.disassociate_address(public_ip=public_ip, association_id=association_id , dry_run=False)     

#dis_eip_associate('5.2.29.7')

def release_ip(public_ip):
    ec2 = boto.ec2.connect_to_region(region)
    address = ec2.get_all_addresses(addresses=[public_ip])
    association_id = address[0].association_id
    allocation_id = address[0].allocation_id
    if association_id == None:
        #ec2.release_address(public_ip=public_ip, allocation_id=allocation_id, dry_run=False)
        ec2.release_address(public_ip=None, allocation_id=allocation_id)
    else:
        print 'The %s ip is be used' % public_ip

release_ip('5.2.29.7')



