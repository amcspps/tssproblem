import numpy as np
import pygad

def fitness_func(solution, solution_idx):
    return np.sum(solution)

#constants
red_lower_bound, red_upper_bound = 30, 60
yellow_lower_bound, yellow_upper_bound = -5, 5
green_lower_bound, green_upper_bound = 30, 60

#num_yellow_fields = 10

#yellow_bounds = np.array([[yellow_lower_bound, yellow_upper_bound]] * num_yellow_fields)

#variable_bounds = np.vstack([[red_lower_bound, red_upper_bound], yellow_bounds, [green_lower_bound, green_upper_bound]])

#gene_types = ['int'] * variable_bounds.shape[0]

#ga_instance = pygad.GA(num_generations=50, num_parents_mating=2, fitness_func=fitness_func,
#                       sol_per_pop=10, num_genes=len(variable_bounds), gene_space=variable_bounds, gene_type=gene_types)

#ga_instance.run()

#best_solution, best_fitness_value, best_solution_idx = ga_instance.best_solution()

#print("Best Solution (rounded to integers):", best_solution.astype(int))
#print("Best Fitness Value:", best_fitness_value)
#print("Generation Index:", best_solution_idx)