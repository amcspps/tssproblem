import numpy as np
import pygad
import utils
import subprocess
import xml.etree.ElementTree as ET
import sys
import time 
#genetic utils 

def set_gene_space(xml_file):
    gene_space = []

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for tl_logic in root.findall(".//tlLogic"):
        for phase in tl_logic.findall("phase"):
            if "y" in phase.attrib["state"]:
                gene_space.append(3)
            else:
                gene_space.append({'low': 30, 'high': 60})
    return gene_space

def on_generation(ga_instance, **kwargs):
    times = kwargs.get('times')
    prev_generation_time = times[-1]
    cur_generation_time = time.time()
    times.append(cur_generation_time) #current generation time logging
    best_solution, best_fitness_value, best_solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
    utils.dump_data(f"{utils.BASEDIR}/{kwargs.get('folder_name')}/res_{utils.gen_name}/results/{utils.ch_iter_time}.csv",
                    [abs(best_fitness_value), ga_instance.generations_completed, round(cur_generation_time-prev_generation_time, 2)]) #cost-history-iteration-time log

#end utils

def fitness_func(ga_instance, solution, solution_idx, **kwargs): 
    #parameters preparation
    iter_id = utils.generate_id()
    output_file = f"{utils.BASEDIR}/{kwargs.get('folder_name')}/res_gen/output/statistic_output_{iter_id}.xml"
    additional_file = f"{utils.BASEDIR}/{kwargs.get('folder_name')}/res_gen/additional/tl_logic_{iter_id}.xml"
    utils.create_new_logic(net_input=kwargs.get('net_file'), additional_output=additional_file, solution=solution)

    command = [utils.sumo_executable,
        '-c', kwargs.get('sumocfg_file'),
        '--statistic-output', output_file,
        '--additional-files', additional_file,
        '--time-to-teleport', utils.time_to_teleport,
        '--no-warnings', 't',
        '--no-step-log', 't',
        '-e', utils.last_simulation_step
    ]
    #----------------------
    process = subprocess.Popen(command)
    process.wait()
    fitness_value = utils.get_total_waiting_time(output_file)
    return -fitness_value


def main(argv):
    if len(argv) != 2:
        print('Usage: python gen.py <simulation-folder-name (for example: "medium")>')
        sys.exit(1)
    else:
        simulation_name = argv[1] 
        gene_type = int
        gene_space = set_gene_space(utils.net_dict.get(simulation_name))
        generation_times = [time.time(), ]
        ff_wrapper = lambda ga_instance, solution, solution_idx: fitness_func(ga_instance, 
                                                                              solution, 
                                                                              solution_idx, 
                                                                              net_file=utils.net_dict.get(simulation_name), 
                                                                              folder_name = simulation_name,
                                                                              sumocfg_file = utils.sumocfg_dict.get(simulation_name))
        
        og_wrapper = lambda ga_instance: on_generation(ga_instance,
                                                       folder_name=simulation_name,
                                                       times=generation_times)
        ga_instance = pygad.GA(num_generations=2000,
                                num_parents_mating=2, 
                                fitness_func=ff_wrapper,
                                sol_per_pop=16,
                                num_genes=len(gene_space),
                                gene_space=gene_space,
                                gene_type=gene_type,
                                parallel_processing=16,
                                save_best_solutions=True,
                                on_generation=og_wrapper
                                )
        ga_instance.run()
    
if __name__ == "__main__":
    main(sys.argv)