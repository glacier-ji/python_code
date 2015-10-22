#!/usr/bin/env python

import boto
import os

from boto import ec2

def show_co(region):

    ec2 = boto.ec2.connect_to_region(region)

    instances = ec2.get_only_instances()
    
    for ins in instances:
        co = ins.get_console_output()

        with open('ins.log', 'a+') as f:
            f.write(str(ins) + '\n')
            f.write(co.output)

show_co('cn-north-1')



#ec2 = boto.ec2.connect_to_region('cn-north-1')

#instance = ec2.get_all_instances()[0].instances[0]

#co = instance.get_console_output()

#with open('ins.log', 'a+') as f:
#    f.write(co.output)

