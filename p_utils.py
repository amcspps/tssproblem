import xml.etree.ElementTree as ET
import numpy as np

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

    return np.array(lower_bounds), np.array(upper_bounds)
#test:1

#lower_bounds, upper_bounds = set_bounds("/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml")
#print('lower')
#print(lower_bounds)
#print('upper')
#print(upper_bounds)

#print(len(lower_bounds))
#print(len(upper_bounds))
