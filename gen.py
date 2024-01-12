import numpy as np
import pygad
import utils
import subprocess
import xml.etree.ElementTree as ET
import sys

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

#end utils

def fitness_func(ga_instance, solution, solution_idx, **kwargs): 
    #parameters preparation
    output_file = f"/home/pavel/dev/diplom/tssproblem/{kwargs.get('folder_name')}/output/statistic_output_{utils.generate_id()}.xml"
    additional_file = f"/home/pavel/dev/diplom/tssproblem/{kwargs.get('folder_name')}/additional/tl_logic_{utils.generate_id()}.xml"
    utils.create_new_logic(net_input=kwargs.get('net_file'), additional_output=additional_file, solution=solution)

    command = [utils.sumo_executable,
        '-c', kwargs.get('sumocfg_file'),
        '--statistic-output', output_file,
        '--additional-files', additional_file,
        '--time-to-teleport', utils.time_to_teleport,
        '--no-warnings',
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
        ff_wrapper = lambda ga_instance, solution, solution_idx: fitness_func(ga_instance, 
                                                                              solution, 
                                                                              solution_idx, 
                                                                              net_file=utils.net_dict.get(simulation_name), 
                                                                              folder_name = simulation_name,
                                                                              sumocfg_file = utils.sumocfg_dict.get(simulation_name))
        ga_instance = pygad.GA(num_generations=10,
                                num_parents_mating=4, 
                                fitness_func=ff_wrapper,
                                sol_per_pop=16,
                                num_genes=len(gene_space),
                                gene_space=gene_space,
                                gene_type=gene_type,
                                parallel_processing=16)
        ga_instance.run()
        best_solution, best_fitness_value, best_solution_idx = ga_instance.best_solution()


if __name__ == "__main__":
    main(sys.argv)