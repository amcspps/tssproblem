import numpy as np
import pyswarms as ps
import p_utils as utils
import newutils
import subprocess
from concurrent.futures import ThreadPoolExecutor

net_file = "/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml"
sumo_executable = '/usr/bin/sumo'
sumocfg_file = '/home/pavel/dev/diplom/tssproblem/medium/sumo/osm.sumocfg'
time_to_teleport = str(150)
last_simulation_step = str(5000)
def evaluate_particle(particle):
    iter_id = newutils.generate_id() #TODO: unique id
    output_file = f'/home/pavel/dev/diplom/tssproblem/output/statistic_output_{iter_id}.xml'
    additional_file = f'/home/pavel/dev/diplom/tssproblem/additional/tl_logic_{iter_id}.xml'
    newutils.create_new_logic(net_input=net_file, additional_output=additional_file, solution=np.round(particle))
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
    fitness_value = newutils.get_total_waiting_time(output_file)
    return fitness_value

def fitness_func(swarm): #has to return ndarray of costs
    with ThreadPoolExecutor() as executor:
        fitness_values = list(executor.map(evaluate_particle, swarm))

    return np.array(fitness_values)


#pso preparation
lower_bounds, upper_bounds = utils.create_bounds(net_file)
num_variables = len(lower_bounds)
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9} 
optimizer = ps.single.GlobalBestPSO(n_particles=16, dimensions=num_variables, options=options, bounds=(lower_bounds, upper_bounds))
best_cost, best_position = optimizer.optimize(fitness_func, iters=10)
print(optimizer.cost_history)
#print(optimizer.pos_history)
print("wtf values are: ", best_cost)


