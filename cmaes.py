import cma
import numpy as np
import c_utils as utils
import newutils
import subprocess
from concurrent.futures import ProcessPoolExecutor

net_file = "/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml"
sumo_executable = '/usr/bin/sumo'
sumocfg_file = '/home/pavel/dev/diplom/tssproblem/medium/sumo/osm.sumocfg'
time_to_teleport = str(150)
last_simulation_step = str(5000)


def fitness_func(solution):
    iter_id = newutils.generate_id() #TODO: unique id
    output_file = f'/home/pavel/dev/diplom/tssproblem/output/statistic_output_{iter_id}.xml'
    additional_file = f'/home/pavel/dev/diplom/tssproblem/additional/tl_logic_{iter_id}.xml'
    newutils.create_new_logic(net_input=net_file, additional_output=additional_file, solution=np.round(solution))
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

opts = utils.create_bounds(xml_file=net_file)
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

print("Solution History:")
for solution, fitness in zip(es.result_pretty, es.result.frecent):
    print(f"Solution: {solution}, Fitness: {fitness}")