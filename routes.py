import subprocess
import os
import utils
import argparse
import shutil
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Generate routes for simulation')
parser.add_argument('--sudo', action='store_true', help='Check if the script was started with sudo')
parser.add_argument('-n', type=str, default='medium', help='Simulation name')
parser.add_argument('-c', type=str, default='51', help='Number of iterations (default: 50)')
args = parser.parse_args()

current_dir = os.path.join(os.getcwd(), args.n)

od2trips_dir = os.path.join(current_dir, 'od2trips')
od2trips_cfg = os.path.join(od2trips_dir, 'od2trips.config.xml')
od_matrix = os.path.join(od2trips_dir, 'from_to.taz.xml')
od2trips_out = os.path.join(od2trips_dir, 'trips.odtrips.xml')


duaiterate_path = '/usr/share/sumo/tools/assign/duaIterate.py'
iterations_path = '/mnt/tss-inter-logs/iterations'
net_path = os.path.join(current_dir, 'net','osm.net.xml')

def update_sumocfg(index):
    xml_file = os.path.join(current_dir, 'sumo', 'osm.sumocfg')
    tree = ET.parse(xml_file)
    root = tree.getroot()
    route_files_element = root.find(".//route-files")
    new_value = os.path.join(current_dir, 'sumo', f'trips.odtrips_{index}.rou.xml')  # Specify the new value here
    route_files_element.set("value", new_value)
    tree.write(xml_file)

def main():
    if args.sudo or utils.is_started_with_sudo():
        subprocess.run(['python', 'memory.py', '-u'])
        subprocess.run(['python', 'memory.py', '-m', '-s', str(4096)])
        subprocess.run(["od2trips", "-c", od2trips_cfg, "-n", od_matrix, "-o", od2trips_out])

        if(not os.path.isdir(iterations_path)):
            os.mkdir(iterations_path)

        os.chdir(iterations_path)
        subprocess.run(['python', duaiterate_path, '-n', net_path, '-t', od2trips_out, '-l', str(args.c)])

        directories = [d for d in os.listdir(iterations_path) if os.path.isdir(os.path.join(iterations_path, d))]
        directories.sort(key=lambda x: int(x))
        last_ind = directories[-1]


        for file in os.listdir(os.path.join(current_dir, 'sumo')):
            if file.startswith('trips.odtrips'):
                file_path = os.path.join(current_dir, 'sumo', file)
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

        subprocess.run(['cp', os.path.join(iterations_path, last_ind, f'trips.odtrips_{last_ind}.rou.xml'), os.path.join(current_dir, 'sumo')])
        update_sumocfg(last_ind)
        for directory in directories:
            directory_path = os.path.join(iterations_path, directory)
            print("Deleting directory:", directory_path)
            shutil.rmtree(directory_path)
        os.chdir(os.path.join(current_dir, '..'))
        subprocess.run(['python', 'memory.py', '-u'])
    else:
        print("usage: sudo python memory.py <args>")    

if __name__ == '__main__':
    main()
