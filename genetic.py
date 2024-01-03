import random
import traci
from multiprocessing import Pool
# Constants
NUM_TRAFFIC_LIGHTS = 1
PHASES_PER_LIGHT = 4

# Function to initialize a random chromosome
def initialize_chromosome():
    return [random.randint(10, 60) for _ in range(NUM_TRAFFIC_LIGHTS * PHASES_PER_LIGHT)]

# Function to evaluate the fitness of a chromosome
def evaluate_fitness(chromosome):
    # Connect to SUMO and start the simulation
    traci.start(["/usr/bin/sumo", "-c", "/home/pavel/dev/diplom/tssproblem/sumo/simulation.sumocfg"])
    
    try:
        # Set initial signal timings
        set_signal_timings(chromosome)

        # Simulate the traffic and get waiting times
        total_waiting_time = simulate_traffic()
    finally:
        # Stop the simulation and disconnect from SUMO
        traci.close()

    return total_waiting_time

def evaluate_fitness_parallel(chromosome):
    with Pool() as pool:
        fitness_values = pool.map(evaluate_fitness, chromosome)
    return fitness_values

# Function to set signal timings using TraCI
def set_signal_timings(chromosome):
    for light in range(NUM_TRAFFIC_LIGHTS):
        light_id = f"traffic_light_{light}"
        
        # Extract phase durations from the chromosome
        phase_durations = chromosome[light * PHASES_PER_LIGHT : (light + 1) * PHASES_PER_LIGHT]

        program_logic = traci.trafficlight.Logic(
            programID="0",
            type=traci.constants.TRAFFICLIGHT_TYPE_STATIC,
            currentPhaseIndex=0,
            phases=(
                traci.trafficlight.Phase(duration=phase_durations[0], state='GrGr'),
                traci.trafficlight.Phase(duration=phase_durations[1], state='yryr'),
                traci.trafficlight.Phase(duration=phase_durations[2], state='rGrG'),
                traci.trafficlight.Phase(duration=phase_durations[3], state='ryry'),
            )
        )
        traci.trafficlight.setProgramLogic(light_id, program_logic)

# Function to simulate traffic and get waiting times using TraCI
def simulate_traffic(simulation_steps=4000):
    total_waiting_time = 0

    for _ in range(simulation_steps):
        traci.simulationStep()

        # Get waiting times for each vehicle
        vehicle_ids = traci.vehicle.getIDList()
        waiting_times = {vehicle_id: traci.vehicle.getWaitingTime(vehicle_id) for vehicle_id in vehicle_ids}

        # Accumulate total waiting time
        total_waiting_time += sum(waiting_times.values())

    return total_waiting_time

# Function to perform crossover between two parent chromosomes
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Function to perform mutation on a chromosome
def mutate(chromosome, mutation_rate=0.1):
    mutated_chromosome = chromosome.copy()
    for i in range(len(mutated_chromosome)):
        if random.random() < mutation_rate:
            mutated_chromosome[i] = random.randint(10, 60)
    return mutated_chromosome

# Main genetic algorithm
def genetic_algorithm(population_size, num_generations):
    population = [initialize_chromosome() for _ in range(population_size)]

    for generation in range(num_generations):
        
        # Selection
        selected_indices = random.sample(range(population_size), k=population_size // 2 * 2)  # Ensure an even number
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

        # Evaluate fitness //TODO: multithread
        #fitness_values = [evaluate_fitness(chromosome) for chromosome in combined_population]

        fitness_values = evaluate_fitness_parallel(combined_population)

        # Select the top individuals for the next generation
        top_indices = sorted(range(len(combined_population)), key=lambda x: fitness_values[x])[:population_size]
        population = [combined_population[i] for i in top_indices]

    # Return the best solution
    best_solution_index = min(range(population_size), key=lambda x: fitness_values[x])
    return population[best_solution_index]

# Example usage
#print(evaluate_fitness([10, 10, 12, 10]))
best_solution = genetic_algorithm(population_size=16, num_generations=20)
print("best traffic signal timings:", best_solution, "provides time:", evaluate_fitness(best_solution))