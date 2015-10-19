#!/usr/bin/env python


import boto
from boto import ec2
from boto.exception import EC2ResponseError

try:
    conn = ec2.connect_to_region('ap-southeast-1')
    regions = conn.get_all_regions()
except EC2ResponseError as e:
    print str(e)

for reg in regions:
    conn = ec2.connect_to_region(reg.name)
    ins = conn.get_only_instances()
    add = conn.get_all_addresses()
    vol = conn.get_all_volumes()
    image = conn.get_all_images()
    snap = conn.get_all_snapshots()
    if ins:
        print 'This %s  no clean, do it now!' % reg
    elif add:
        print 'This %S have address no clean'  %reg
    elif vol:
        print 'This %s have volumes' % reg
    elif image:
        print 'This %s have images' % reg
    elif snap:
        print 'This %s have snapshots' % reg
    else:
        print '%s have no resource' % reg

