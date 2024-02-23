import numpy as np
from scipy.optimize import dual_annealing
from scipy.optimize import Bounds
import subprocess
import sys
import utils
import xml.etree.ElementTree as ET
from functools import partial

#scipy-method-utils
def create_bounds(xml_file):
    lower_bounds = []
    upper_bounds = []

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for tl_logic in root.findall(".//tlLogic"):
        for phase in tl_logic.findall("phase"):
            if "y" not in phase.attrib["state"]:
                lower_bounds.append(30)
                upper_bounds.append(60)

    bounds = Bounds(lower_bounds, upper_bounds)
    return bounds
#------------------

def fitness_func(solution, **kwargs): 
    iter_id = utils.generate_id()
    output_file = f"/mnt/tss-inter-logs/{kwargs.get('folder_name')}/statistic_output_{iter_id}.xml"
    additional_file = f"/mnt/tss-inter-logs/{kwargs.get('folder_name')}/tl_logic_{iter_id}.xml"
    utils.create_new_logic(net_input=kwargs.get('net_file'), additional_output=additional_file, solution=np.round(solution))
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
    subprocess.run(['rm', additional_file, output_file])
    return fitness_value


def main(argv):
    if len(argv) != 1:
        print('Usage: python gen.py <simulation-folder-name (for example: "medium")>')
        sys.exit(1)
    else:
        simulation_name = 'medium' #argv[1]
        bounds = create_bounds(xml_file=utils.net_dict.get(simulation_name))

        ff_partial = partial(fitness_func,
                             net_file=utils.net_dict.get(simulation_name),
                             folder_name=simulation_name,
                             sumocfg_file=utils.sumocfg_dict.get(simulation_name))


        res = dual_annealing(ff_partial, bounds, no_local_search=True, maxiter=400)
        print(res.fun, res.message)
if __name__ == "__main__":
    main(sys.argv)