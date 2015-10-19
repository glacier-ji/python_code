#!/usr/bin/env python

import math, os
import boto
from filechunkio import FileChunkIO

#Connect to S3
c = boto.connect_s3()
b = c.get_bucket('mybucket')

# Get file info
source_path = 'path/to/your/file.ext'
source_size = os.stat(source_path).st_size

#Create a multipart upload request
mp = b.initiate_multipart_upload(os.path.basename(source_path))

# Use a chunk size of 50 MiB (feel free to change this)
chunk_size = 52428800
chunk_count = int(math.ceil(source_size / float(chunk_size)))


# Send the file parts, using FileChunkIO to create a file-like object
# that points to a certain byte range within the original file. We
# set bytes to never exceed the original file size.
for i in range(chunk_count):
    offset = chunk_size * i
    bytes = min(chunk_size, source_size - offset)
    with FileChunkIO(source_path, 'r', offset=offset, bytes=bytes) as fp:
        mp.upload_part_from_file(fp, part_num=i + 1)

# Finish the upload
mp.complete_upload()
    
