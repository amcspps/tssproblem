import numpy as np
import pygad
import newutils
import subprocess
import os
import time

net_file = "/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml"
sumo_executable = '/usr/bin/sumo'
sumocfg_file = '/home/pavel/dev/diplom/tssproblem/medium/sumo/osm.sumocfg'
time_to_teleport = str(150)
last_simulation_step = str(5000)

#TODO: net change (argc argv)
#TODO: reduce iterations

def fitness_func(ga_instance, solution, solution_idx): 
    iter_id = newutils.generate_id() #TODO: unique id

    output_file = f'/home/pavel/dev/diplom/tssproblem/output/statistic_output_{iter_id}.xml'
    additional_file = f'/home/pavel/dev/diplom/tssproblem/additional/tl_logic_{iter_id}.xml'
    newutils.create_new_logic(net_input=net_file, additional_output=additional_file, solution=solution)
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
    return -fitness_value


gene_type = int

gene_space = newutils.set_gene_space(net_file)

ga_instance = pygad.GA(num_generations=10,
                        num_parents_mating=4, 
                        fitness_func=fitness_func,
                        sol_per_pop=16,
                        num_genes=len(gene_space),
                        gene_space=gene_space,
                        gene_type=gene_type,
                        parallel_processing=16,
                        )

ga_instance.run()

best_solution, best_fitness_value, best_solution_idx = ga_instance.best_solution()

print("Best Solution:", best_solution)
print("Best Fitness Value:", best_fitness_value)
print("Generation Index:", best_solution_idx)