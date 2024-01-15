import numpy as np
import pyswarms as ps
import utils
import subprocess
from concurrent.futures import ProcessPoolExecutor
import xml.etree.ElementTree as ET
import sys
from functools import partial

#pso utils

def create_bounds(xml_file):
    lower_bounds = []
    upper_bounds = []

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for tl_logic in root.findall(".//tlLogic"):
        for phase in tl_logic.findall("phase"):
            if "y" in phase.attrib["state"]:
                lower_bounds.extend([2.95])
                upper_bounds.extend([3.05])
            else:
                lower_bounds.extend([30])
                upper_bounds.extend([60])

    return np.array(lower_bounds), np.array(upper_bounds)

#end utils

def evaluate_particle(particle, **kwargs):
    iter_id = utils.generate_id()
    output_file = f"/home/pavel/dev/diplom/tssproblem/{kwargs.get('folder_name')}/res_pso/output/statistic_output_{iter_id}.xml"
    additional_file = f"/home/pavel/dev/diplom/tssproblem/{kwargs.get('folder_name')}/res_pso/additional/tl_logic_{iter_id}.xml"
    utils.create_new_logic(net_input=kwargs.get('net_file'), additional_output=additional_file, solution=np.round(particle))
    command = [utils.sumo_executable,
        '-c', kwargs.get('sumocfg_file'),
        '--statistic-output', output_file,
        '--additional-files', additional_file,
        '--time-to-teleport', utils.time_to_teleport,
        '--no-warnings',
        '-e', utils.last_simulation_step
    ]

    process = subprocess.Popen(command)
    process.wait()
    fitness_value = utils.get_total_waiting_time(output_file)
    return fitness_value

def fitness_func(swarm, **kwargs):
    partial_evaluate_particle = partial(evaluate_particle, **kwargs)
    with ProcessPoolExecutor() as executor:
        fitness_values = list(executor.map(partial_evaluate_particle, swarm))

    return np.array(fitness_values)

def main(argv):
    if len(argv) != 2:
        print('Usage: python gen.py <simulation-folder-name (for example: "medium")>')
        sys.exit(1)
    else:
        simulation_name = argv[1] 
        lower_bounds, upper_bounds = create_bounds(utils.net_dict.get(simulation_name))
        num_variables = len(lower_bounds)
        options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9} 
        optimizer = ps.single.GlobalBestPSO(n_particles=8, dimensions=num_variables, options=options, bounds=(lower_bounds, upper_bounds))
        ff_wrapper = lambda swarm: fitness_func(swarm=swarm, 
                                                net_file=utils.net_dict.get(simulation_name), 
                                                folder_name=simulation_name,
                                                sumocfg_file=utils.sumocfg_dict.get(simulation_name))
        best_cost, best_position = optimizer.optimize(ff_wrapper, iters=5)
    print(optimizer.cost_history)
    print("best cost values are: ", best_cost)
if __name__ == "__main__":
    main(sys.argv)