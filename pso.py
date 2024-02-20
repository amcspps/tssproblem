import numpy as np
import pyswarms as ps
import utils
import subprocess
from concurrent.futures import ProcessPoolExecutor
import xml.etree.ElementTree as ET
import sys
from functools import partial
import time
import pdb

#pso utils

def create_bounds(xml_file):
    lower_bounds = []
    upper_bounds = []

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for tl_logic in root.findall(".//tlLogic"):
        for phase in tl_logic.findall("phase"):
            if "y" not in phase.attrib["state"]:
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
        '--no-warnings', 't',
        '--no-step-log', 't',
        '-e', utils.last_simulation_step
    ]

    process = subprocess.Popen(command)
    process.wait()
    fitness_value = utils.get_total_waiting_time(output_file)
    return fitness_value

def fitness_func(swarm, **kwargs):
    times = kwargs.get('times')
    partial_evaluate_particle = partial(evaluate_particle, **kwargs)
    with ProcessPoolExecutor(12) as executor:
        fitness_values = list(executor.map(partial_evaluate_particle, swarm))
    cur_swarm_time = time.time()
    times.append(cur_swarm_time) #current swarm time logging 
    return np.array(fitness_values)

def main(argv):
    if len(argv) != 1:
        print('Usage: python gen.py <simulation-folder-name (for example: "medium")>')
        sys.exit(1)
    else:
        simulation_name = 'medium' #argv[1]
        swarm_times = [time.time(), ]
        lower_bounds, upper_bounds = create_bounds(utils.net_dict.get(simulation_name))
        num_variables = len(lower_bounds)
        options = {'c1': 2.05, 'c2': 2.05, 'w': 0.72984} #global-best-pso
        #options = {'c1': 1.5, 'c2': 1.5, 'w': 0.7, 'k': 22, 'p': 2} #local-best-pso 
        
        optimizer = ps.single.GlobalBestPSO(n_particles=880, dimensions=num_variables, options=options, oh_strategy={ "w":'exp_decay', "c1":'nonlin_mod',"c2":'lin_variation'}, bounds=(lower_bounds, upper_bounds))
        ff_wrapper = lambda swarm: fitness_func(swarm=swarm, 
                                                net_file=utils.net_dict.get(simulation_name), 
                                                folder_name=simulation_name,
                                                sumocfg_file=utils.sumocfg_dict.get(simulation_name),
                                                times=swarm_times)
        best_cost, best_position = optimizer.optimize(ff_wrapper, iters=400, verbose=False)
    data = zip(optimizer.cost_history, range(1, len(optimizer.cost_history) + 1), [round(cur - prev, 2) for prev, cur in zip(swarm_times, swarm_times[1:])])
    for row in data:
        utils.dump_data(f"{utils.BASEDIR}/{simulation_name}/res_{utils.pso_name}/results/{utils.ch_iter_time}.csv",
                    row)
if __name__ == "__main__":
    main(sys.argv)