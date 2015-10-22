import boto
from boto import ec2
import time

region = 'cn-north-1'

def Back_volumes():
    ec2 = ec2 = boto.ec2.connect_to_region(region)
    volumes = ec2.get_all_volumes()
    snaps = [ v.create_snapshot() for v in volumes ]
    print snaps


Back_volumes()
