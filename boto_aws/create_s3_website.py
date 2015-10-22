#!/usr/bin/env python

import os
import boto
import time

def create_bucket(bucket_name):
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)
    if bucket:
        print 'Bucket (%s) already exists' % bucket_name
    else:
        try:
            bucket = s3.create_bucket(bucket_name)
        except s3.provider.storage_create_error, e:
            print 'Bucket (%s) is owned by another user' % bucket_name
    return bucket



def upload_website(bucket_name, website_dir, index_file, error_file=None):
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)
    bucket.set_canned_acl('public-read')

    for root, dirs, files in os.walk(website_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, website_dir)
            key = bucket.new_key(rel_path)
            key.content_type = 'txtx/html'
            key.set_contents_from_filename(full_path, policy='pulic-read')

    bucket.configure_websiet(index_file, error_file)

    time.sleep(5)

    print 'You can access your website at:'
    print bucket.get_website_endpoint()

create_bucket('bicherweb')


upload_website('bicherweb', 'html', 'index.html')
