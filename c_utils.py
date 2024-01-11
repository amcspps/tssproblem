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

    bounds_dict = {'bounds': [lower_bounds, upper_bounds]}
    return bounds_dict

#test:1
#xml_file = "/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml"
#result = create_bounds(xml_file=xml_file)
#print(result)
#print(len(result.get('bounds')[0]))