import boto
from boto import ec2
import time

region = 'cn-north-1'

def restore_volumes():
    ec2 = boto.ec2.connect_to_region(region)
    volume_id = 'vol-f95619ec'
    bad_volume = ec2.get_all_volumes([volume_id])[0]
    snaps = bad_volume.snapshots() 
    snaps.sort(key=lambda snap: snap.start_time)
    latest_snap = snaps[-1]
    new_volume = ec2.create_volume(bad_volume.size, bad_volume.zone, latest_snap)

restore_volumes()
