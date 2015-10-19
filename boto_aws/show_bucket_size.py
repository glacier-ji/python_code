
#!/usr/bin/env python

import boto

def bucket_size(bucket_name):
    s3 = boto.connect_s3()
    total_bytes = 0
    bucket = s3.lookup(bucket_name)
    if bucket:
        for key in bucket:
            total_bytes = total_bytes + key.size
            print key, key.size
    else:
        print 'Warning: no find %s!' % bucket_name
    return total_bytes


total_size = bucket_size("bicherweb")
print total_size

