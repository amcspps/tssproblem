import random
import traci
from multiprocessing import Pool
import utils
import subprocess

def initialize_chromosome(tlLogic_phases):
    chromosome = []
    for light_phases in tlLogic_phases.values():
        chromosome.extend([random.randint(10, 60) for _ in range(len(light_phases))])
    return chromosome

def evaluate_fitness(chromosome, tlLogic_phases):
    traci.start(["/usr/bin/sumo", "-c", "/home/pavel/dev/diplom/tssproblem/test/sumo/simulation.sumocfg"])
    #traci.start(["/usr/bin/sumo", "-c", "/home/pavel/dev/diplom/tssproblem/medium/sumo/osm.sumocfg", "--no-warnings"])
    try:
        set_signal_timings(chromosome, tlLogic_phases=tlLogic_phases)
        total_waiting_time = simulate_traffic()
        with open('conv_log.txt','a') as file:
            file.write(str(total_waiting_time) + '\n')

    finally:
        traci.close()

    return total_waiting_time

def evaluate_fitness_parallel(chromosomes, tlLogic_phases):
    with Pool() as pool:
        args = [(chromosome, tlLogic_phases) for chromosome in chromosomes]
        fitness_values = pool.starmap(evaluate_fitness, args)
    return fitness_values
  
def set_signal_timings(chromosome, tlLogic_phases):
    for light_id, phases in tlLogic_phases.items():
        generated_phases_durations = chromosome[:len(phases)]
        chromosome[len(phases):]
        program_logic = traci.trafficlight.Logic(
            programID="0",
            type=traci.constants.TRAFFICLIGHT_TYPE_STATIC,
            currentPhaseIndex=0,
            phases=tuple(
                traci.trafficlight.Phase(duration=duration, state=state)
                for duration, state in zip(generated_phases_durations, (state for _, state in phases))
            )
        )
        traci.trafficlight.setProgramLogic(light_id, program_logic)
        #TODO:for loop here with setProgramLogic
def simulate_traffic(simulation_steps=4000):
    total_waiting_time = 0

    for _ in range(simulation_steps):
        traci.simulationStep()

        vehicle_ids = traci.vehicle.getIDList()
        waiting_times = {vehicle_id: traci.vehicle.getWaitingTime(vehicle_id) for vehicle_id in vehicle_ids}

        total_waiting_time += sum(waiting_times.values())

    return total_waiting_time

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutate(chromosome, mutation_rate=0.1):
    mutated_chromosome = chromosome.copy()
    for i in range(len(mutated_chromosome)):
        if random.random() < mutation_rate:
            mutated_chromosome[i] = random.randint(10, 60)
    return mutated_chromosome

def genetic_algorithm(population_size, num_generations, id_type_counts, tlLogic_phases):
    population = [initialize_chromosome(tlLogic_phases) for _ in range(population_size)]

    for generation in range(num_generations):
        
        # Selection
        selected_indices = random.sample(range(population_size), k=population_size // 2 * 2) 
        parents = [population[i] for i in selected_indices]

        # Crossover
        offspring = []
        for i in range(0, len(parents), 2):
            child1, child2 = crossover(parents[i], parents[i + 1])
            offspring.extend([child1, child2])

        # Mutation
        offspring = [mutate(child) for child in offspring]

        # Combine parents and offspring
        combined_population = parents + offspring

        # Evaluate fitness: signle-thread 
        #fitness_values = [evaluate_fitness(chromosome) for chromosome in combined_population]
        
        # Evaluate fitness:multithread
        fitness_values = evaluate_fitness_parallel(combined_population, tlLogic_phases)

        # Select the top individuals for the next generation
        top_indices = sorted(range(len(combined_population)), key=lambda x: fitness_values[x])[:population_size]
        population = [combined_population[i] for i in top_indices]

    # Return the best solution
    best_solution_index = min(range(population_size), key=lambda x: fitness_values[x])
    return population[best_solution_index]





utils.cleanup_log_files('sorted_log.txt', 'conv_log.txt')

id_type_counts, tlLogic_phases = utils.tlLogic_loader("/home/pavel/dev/diplom/tssproblem/test/net/straight_cross.net.xml")
#id_type_counts, tlLogic_phases = utils.tlLogic_loader("/home/pavel/dev/diplom/tssproblem/medium/net/osm.net.xml")
best_solution = genetic_algorithm(population_size=16, num_generations=200, id_type_counts=id_type_counts, tlLogic_phases=tlLogic_phases)
print("best traffic signal timings:", best_solution, "provides time:", evaluate_fitness(best_solution, tlLogic_phases))

subprocess.run(['sort', '-n', '-o', 'sorted_log.txt', 'conv_log.txt'])