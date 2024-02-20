import subprocess
import os
import utils
import argparse

target_mount_point = '/mnt/tss-inter-logs'

def is_mounted(target):
    output = subprocess.run(['sudo', 'mount'], capture_output=True, text=True)
    
    for line in output.stdout.splitlines():
        if target in line:
            return True
    
    return False

def directory_exists(directory):
    return os.path.exists(directory)

def create_hierarchy(target_directory):
    subprocess.run(['sudo', 'mkdir', target_directory])
    for name in utils.names_dict:
        subprocess.run(['sudo','mkdir', os.path.join(target_directory, name)])

def mount_tmpfs(target_directory):
    subprocess.run(['sudo', 'mount', '-t', 'tmpfs', '-o', 'size=10M', 'tmpfs', target_directory])
     
def mount():
    if not directory_exists(target_mount_point):
        print(f"{target_mount_point} does not exist.")
        create_hierarchy(target_directory=target_mount_point)
        print(f"{target_mount_point} hierarchy created.")
        mount_tmpfs(target_mount_point)
        print(f"{target_mount_point} has been mounted.")
    else:
        if is_mounted(target_mount_point):
            print(f"{target_mount_point} is already mounted.")
        else:
            mount_tmpfs(target_mount_point)
            print(f"{target_mount_point} has been mounted.")

def unmount():
    result = subprocess.run(['sudo', 'umount','-f', target_mount_point])
    subprocess.run(['sudo', 'rm', '-rf',  target_mount_point])
    print(f"{target_mount_point} has been successfully unmounted. folders deleted.")

parser = argparse.ArgumentParser(description='Manage tmpfs memory mounts')
parser.add_argument('-m', action='store_true', help='Mount tmpfs memory')
parser.add_argument('-u', action='store_true', help='Unmount tmpfs memory and delete directory')
args = parser.parse_args()


if args.m:
    mount()

elif args.u:
    unmount()
else:
    print("No action specified. Use -m to mount or -u to unmount.")