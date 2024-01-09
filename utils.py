import xml.etree.ElementTree as ET
from collections import defaultdict
import time

def cleanup_log_files(sorted_log, conv_log):
    with open(sorted_log, 'w') as file:
        file.write("")
    with open(conv_log, 'w') as file:
        file.write("")


def display_counts_and_phases(id_type_counts, tlLogic_phases):
    print("Counts based on id types:")
    for id_type, count in id_type_counts.items():
        print(f"Number of tlLogic objects with id type '{id_type}': {count}")

    print("\nPhases:")
    phase_counts = defaultdict(int)

    for tl_id, phases in tlLogic_phases.items():
        for phase in phases:
            duration = phase[0]
            state = phase[1]
            phase_counts[(tl_id, state)] += duration

    for (tl_id, state), duration in phase_counts.items():
        print(f"tlLogic {tl_id}, state {state}, duration: {duration}")

def tlLogic_loader(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    id_type_counts = defaultdict(int)
    tlLogic_phases = defaultdict(list)

    for tlLogic in root.findall(".//tlLogic"):
        tl_id = tlLogic.get("id")
        id_type = tl_id.split('_')[0]
        id_type_counts[id_type] += 1

        phases = tlLogic.findall("phase")
        dur_state_list = [(int(phase.get("duration")), phase.get("state")) for phase in phases] 
        tlLogic_phases[tl_id] = dur_state_list

    display_counts_and_phases(id_type_counts, tlLogic_phases)

    return id_type_counts, tlLogic_phases

#start = time.time()
#tlLogic_loader("/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml")
#end = time.time()
#print(f"elapsed: {end-start}")


# def parselogic_test(xml_data):
#     tree = ET.parse(xml_data)
#     root = tree.getroot()
#     print("XML parsing successful")
    
#     # Extract information from the parsed XML tree
#     waiting_counts = [int(tripinfo.get("waitingCount", 0)) for tripinfo in root.findall(".//tripinfo")]
#     mean_waiting_count = sum(waiting_counts) / len(waiting_counts) if waiting_counts else 0
#     print(f"Mean Waiting Count: {mean_waiting_count}", f"count: {len(wai)}")

# start = time.time()
# parselogic_test("/home/pavel/dev/diplom/tssproblem/tripinfo_output.xml")
# end = time.time()
# print(f"elapsed: {end-start}")
