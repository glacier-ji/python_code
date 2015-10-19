#!/usr/bin/env python

import boto

def copyobject(src_bucket, src_keyname, dst_bucket, dst_keyname):
    s3 = boto.connect_s3()
    src_bucket = s3.lookup(src_bucket)
    src_keyname = src_bucket.lookup(src_keyname)
    src_keyname.copy(dst_bucket, dst_keyname, preserve_acl=True)


copyobject("bicher", "install.html", "bicherweb", "install.html")



