import xml.etree.ElementTree as ET
import numpy as np
import uuid
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

BASEDIR = os.getcwd()

#plot-names
ch_iter_time = 'ch_iter_time'
#----------

#simulation-names
medium = 'medium'
commercial = 'commercial'
names = [medium, commercial]
#-----

#exe
sumo_executable = '/usr/bin/sumo'
#--------

#conifigs
sumocfg_dict = {
    medium: f'{BASEDIR}/medium/sumo/osm.sumocfg',
    commercial: f'{BASEDIR}/commercial/sumo/osm.sumocfg',
}
#--------

#net-files
net_dict = {
    medium: f'{BASEDIR}/medium/net/osm.net.xml',
    commercial: f'{BASEDIR}/commercial/net/osm.net.xml',
}
#---------

#simulation args
time_to_teleport = str(-1)
last_simulation_step = str(4500)
#---------------



def create_new_logic(net_input, additional_output, solution):
    tree = ET.parse(net_input)
    root = tree.getroot()
    tl_logics = root.findall('.//tlLogic')
    new_root = ET.Element('additional')

    for tl_logic in tl_logics:
        for phase in tl_logic.findall('.//phase'):
            if "y" not in phase.attrib["state"]: #if phase os "optimizable"
                duration = int(solution[0])
                solution = np.delete(solution, 0)
                phase.set('duration', str(duration))
            else: #yellow constant 3
                phase.set('duration', str(4))
        tl_logic.set('programID', 'generated')

    new_root.extend(tl_logics)
    new_tree = ET.ElementTree(new_root)
    new_tree.write(additional_output)


def get_total_waiting_time(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    vehicle_trip_statistics = root.find(".//vehicleTripStatistics")
    return float(vehicle_trip_statistics.get("waitingTime"))

def generate_id():
    unique_id = str(uuid.uuid4())
    return unique_id

def dump_data(output_path, row):
    with open(output_path, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(row)

def plot(simulation_name, plot_name):
    if plot_name == ch_iter_time:
        csv_data_list = []
        fig, ax = plt.subplots(2, 1, figsize=(8, 6))
        for alg_name in [gen_name, pso_name, cmaes_name]:
            log_path = f"{BASEDIR}/{simulation_name}/res_{alg_name}/results/{plot_name}.csv"
            filename = os.path.basename(os.path.splitext(log_path)[0])
            df = pd.read_csv(log_path)
            df.columns = filename.split('_')
            csv_data_list.append(df)

            ax[0].plot(df['iter'], df['ch'], label= f'{alg_name}')
            ax[0].set_title('cost-history, iterations')
            ax[0].set_xlabel('iterations')
            ax[0].set_ylabel('cost-history')
            ax[0].legend()

            ax[1].plot(df['iter'], df['time'], label= f'{alg_name}')
            ax[1].set_title('time, iterations')
            ax[1].set_xlabel('iterations')
            ax[1].set_ylabel('iteraton time')
            ax[1].legend()

            plt.tight_layout()
        plt.show()

def is_started_with_sudo():
    return 'SUDO_USER' in os.environ

def histogram():
    # Lists to store data
    alg_names = []
    evals_all = []
    sum_times = []
    # Read data from CSV file
    with open(f'{BASEDIR}/commercial/results/results.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            alg_names.append(row['alg-name'])
            evals_all.append(int(row['evals-all']))  # Convert to integer
            sum_times.append(float(row['sum-time']))
    # Create a dictionary to store total evaluations for each algorithm
    total_evals = {}
    total_times = {}
    for alg, evals in zip(alg_names, evals_all):
        total_evals[alg] = total_evals.get(alg, 0) + evals
    for alg, time in zip(alg_names, sum_times):
        total_times[alg] = total_times.get(alg, 0) + time
    # Create histogram
    plt.figure()
    plt.bar(total_evals.keys(), total_evals.values(), alpha=0.5)
    plt.xlabel('Algorithm name')
    plt.ylabel('Total evaluations')
    plt.title('Total evaluations: commercial')
    plt.grid(True)

    plt.figure()
    plt.bar(total_times.keys(), total_times.values(), alpha=0.5)
    plt.xlabel('Algorithm name')
    plt.ylabel('Total times')
    plt.title('Total times: commercial')
    plt.grid(True)
plt.show()
