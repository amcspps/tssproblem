import cma
import numpy as np
import utils
import subprocess
from concurrent.futures import ProcessPoolExecutor
import xml.etree.ElementTree as ET

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

net_file = "/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml"
sumo_executable = '/usr/bin/sumo'
sumocfg_file = '/home/pavel/dev/diplom/tssproblem/medium/sumo/osm.sumocfg'
time_to_teleport = str(150)
last_simulation_step = str(5000)


def fitness_func(solution):
    iter_id = utils.generate_id() #TODO: unique id
    output_file = f'/home/pavel/dev/diplom/tssproblem/output/statistic_output_{iter_id}.xml'
    additional_file = f'/home/pavel/dev/diplom/tssproblem/additional/tl_logic_{iter_id}.xml'
    utils.create_new_logic(net_input=net_file, additional_output=additional_file, solution=np.round(solution))
    command = [sumo_executable,
        '-c', sumocfg_file,
        '--statistic-output', output_file,
        '--additional-files', additional_file,
        '--time-to-teleport', time_to_teleport,
        '--no-warnings',
        '-e', last_simulation_step
    ]

    process = subprocess.Popen(command)
    process.wait()
    fitness_value = utils.get_total_waiting_time(output_file)
    return fitness_value

opts = create_bounds(xml_file=net_file)
dimension = len(opts.get('bounds')[1])

opts['popsize'] = 16

x0 = np.random.uniform(low=opts.get('bounds')[0], high=opts.get('bounds')[1], size=dimension)
sigma = 0.5

es = cma.CMAEvolutionStrategy(x0, sigma, opts)
iter_count = 2
with ProcessPoolExecutor() as executor:
    for _ in range(iter_count):
        solutions = es.ask()
        fitness_values = list(executor.map(fitness_func, solutions))
        es.tell(solutions, fitness_values)

best_solution = es.result.xbest
best_fitness = es.result.fbest

print("Best Solution:", best_solution)
print("Best Fitness:", best_fitness)

