import xml.etree.ElementTree as ET
import numpy as np
import uuid 

#names
test_name = 'test'
medium_name = 'medium'
large_name = 'large'
#-----

#exe
sumo_executable = '/usr/bin/sumo'
#--------

#conifigs
sumocfg_dict = {
    test_name: '/home/pavel/dev/diplom/tssproblem/test/sumo/simulation.sumocfg',
    medium_name: '/home/pavel/dev/diplom/tssproblem/medium/sumo/osm.sumocfg',
    large_name: 'placeholder',
}
#--------

#net-files
net_dict = {
    test_name: '/home/pavel/dev/diplom/tssproblem/test/net/osm.net.xml',
    medium_name: '/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml',
    large_name: 'placeholder',

}
#---------


#simulation args
time_to_teleport = str(150)
last_simulation_step = str(5000)
#---------------



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
        tl_logic.set('programID', 'generated')

    new_root.extend(tl_logics)
    new_tree = ET.ElementTree(new_root)
    new_tree.write(additional_output)
    

def get_total_waiting_time(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    vehicle_trip_statistics = root.find(".//vehicleTripStatistics")
    return float(vehicle_trip_statistics.get("waitingTime"))



def generate_id():
    unique_id = str(uuid.uuid4())
    return unique_id

