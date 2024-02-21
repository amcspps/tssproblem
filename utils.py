import xml.etree.ElementTree as ET
import numpy as np
import uuid
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt


BASEDIR = os.getcwd()

#exe
sumo_executable = '/usr/bin/sumo'
#--------

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
            log_path = f"{BASEDIR}/{simulation_name}/results/{plot_name}.csv"
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