#!/usr/bin/env python

import boto
from boto import bucket

def bucket_size(bucket_name):
    s3 = boto.connect_s3()
    total_bytes = 0
    bucket = s3.get_key(bucket_name)
    if bucket:
        for key in bucket:
            total_bytes = total_bytes + key.size
    else:
        print 'Warning: no find %s!' % bucket_name
    return total_bytes


total_size = bucket_size("test01")
print total_size

    
