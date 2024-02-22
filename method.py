import numpy as np
from scipy.optimize import dual_annealing
from scipy.optimize import Bounds

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

def main(argv):
    if len(argv) != 1:
        print('Usage: python gen.py <simulation-folder-name (for example: "medium")>')
        sys.exit(1)
    else:
        simulation_name = 'medium' #argv[1]
        bounds = create_bounds(xml_file=utils.net_dict.get(simulation_name))

        ff_partial = partial(utils.fitness_func,
                             net_file=utils.net_dict.get(simulation_name),
                             folder_name=simulation_name,
                             sumocfg_file=utils.sumocfg_dict.get(simulation_name))


        res = dual_annealing(ff_partial, bounds, no_local_search=True, maxiter=400)
        print(res.fun, res.message)
if __name__ == "__main__":
    main(sys.argv)