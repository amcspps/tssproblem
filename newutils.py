import xml.etree.ElementTree as ET
import random
import numpy as np
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

def create_new_logic(net_input, additional_output, solution):
    tree = ET.parse(net_input)
    root = tree.getroot()

    tl_logics = root.findall('.//tlLogic')

    new_root = ET.Element('additional')

    for tl_logic in tl_logics:
        for phase in tl_logic.findall('.//phase'):
            duration = int(solution[0])
            solution = np.delete(solution, 0)
            phase.set('duration', str(int(duration)))

    new_root.extend(tl_logics)

    new_tree = ET.ElementTree(new_root)

    new_tree.write(additional_output)
    

def get_total_waiting_time(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    vehicle_trip_statistics = root.find(".//vehicleTripStatistics")
    return float(vehicle_trip_statistics.get("waitingTime"))

def generate_id():
    return random.randint(1, 10000)
#test:1
#gene_space = set_gene_space("/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml")

#print(gene_space)
#print(len(gene_space))

#print(get_total_waiting_time("/home/pavel/dev/diplom/tssproblem/output/statistic_output_1.xml"))

#test:2
#net_file = "/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml"
#additional_file = f'/home/pavel/dev/diplom/tssproblem/additional/tl_logic_2.xml'

#solution = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38])
#create_new_logic(net_input=net_file,additional_output=additional_file, solution=solution)
