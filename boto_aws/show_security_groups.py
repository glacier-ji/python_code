#!/usr/bin/env python

import boto
from boto import ec2

conn=ec2.connect_to_region('cn-north-1')
for group in conn.get_all_security_groups():
    for rule in group.rules:
        for grant in rule.grants:
            print group, rule,grant
