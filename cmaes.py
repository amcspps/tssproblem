import cma
import numpy as np
import utils
import subprocess
from concurrent.futures import ProcessPoolExecutor
import xml.etree.ElementTree as ET
import sys
from functools import partial
#cmaes utils

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

    bounds_dict = {'bounds': [lower_bounds, upper_bounds]}
    return bounds_dict

#end utils

def fitness_func(solution, **kwargs):
    output_file = f"/home/pavel/dev/diplom/tssproblem/{kwargs.get('folder_name')}/output/statistic_output_{utils.generate_id()}.xml"
    additional_file = f"/home/pavel/dev/diplom/tssproblem/{kwargs.get('folder_name')}/additional/tl_logic_{utils.generate_id()}.xml"
    utils.create_new_logic(net_input=kwargs.get('net_file'), additional_output=additional_file, solution=np.round(solution))
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

def main(argv):
    if len(argv) != 2:
        print('Usage: python gen.py <simulation-folder-name (for example: "medium")>')
        sys.exit(1)
    else:
        simulation_name = argv[1]
        #parameters preparation
        opts = create_bounds(xml_file=utils.net_dict.get(simulation_name))
        dimension = len(opts.get('bounds')[1])
        opts['popsize'] = 16
        x0 = np.random.uniform(low=opts.get('bounds')[0], high=opts.get('bounds')[1], size=dimension)
        sigma = 0.5
        #----------------------
        es = cma.CMAEvolutionStrategy(x0, sigma, opts)
        iter_count = 1

        ff_partial = partial(fitness_func,
                             net_file=utils.net_dict.get(simulation_name),
                             folder_name=simulation_name,
                             sumocfg_file=utils.sumocfg_dict.get(simulation_name))
        with ProcessPoolExecutor(16) as executor:
            for _ in range(iter_count):
                solutions = es.ask()
                fitness_values = list(executor.map(ff_partial, solutions))
                es.tell(solutions, fitness_values)

        best_solution = es.result.xbest
        best_fitness = es.result.fbest
        print("Best Solution:", best_solution)
        print("Best Fitness:", best_fitness)

if __name__ == "__main__":
    main(sys.argv)