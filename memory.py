import subprocess
import os
import utils
import argparse

target_mount_point = '/mnt/tss-inter-logs'

def is_mounted(target):
    output = subprocess.run(['mount'], capture_output=True, text=True)
    
    for line in output.stdout.splitlines():
        if target in line:
            return True
    
    return False

def directory_exists(directory):
    return os.path.exists(directory)

def create_hierarchy(target_directory):
    subprocess.run(['mkdir', target_directory])
    for name in utils.names_dict:
        subprocess.run(['mkdir', os.path.join(target_directory, name)])

def mount_tmpfs(target_directory):
    subprocess.run(['mount', '-t', 'tmpfs', '-o', 'size=10M', 'tmpfs', target_directory])
     
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
    result = subprocess.run(['umount','-f', target_mount_point])
    subprocess.run(['rm', '-rf',  target_mount_point])
    print(f"{target_mount_point} has been successfully unmounted. folders deleted.")

parser = argparse.ArgumentParser(description='Manage tmpfs memory mounts')
parser.add_argument('--sudo', action='store_true', help='Check if the script was started with sudo')
parser.add_argument('-m', action='store_true', help='Mount tmpfs memory')
parser.add_argument('-u', action='store_true', help='Unmount tmpfs memory and delete directory')
args = parser.parse_args()

def is_started_with_sudo():
    return 'SUDO_USER' in os.environ

if args.sudo or is_started_with_sudo():        
    if args.m:
        mount()
    elif args.u:
        unmount()
    else:
        print("No action specified. Use -m to mount or -u to unmount.")
else:
    print("usage: sudo python script.py")
