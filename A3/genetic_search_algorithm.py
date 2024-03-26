# CS 131 A3
# Written by: Perucy Mussiba
# Date: 12th March 2024
# Purpose: The code below implements genetic algorithm search through a problem that involves packing
#           boxes in a bag to maximize the value of the bag without exceeding the weight limit

import random
import numpy as np

MAX_WEIGHT = 250  # maximum weight the backpack can hold
POPULATION_SIZE = 100  # population size
NUM_BOXES = 12  # number of boxes to choose
CULL_PERCENTAGE = 0.5  # percentage at which a population is reduced or culled
TARGET_FITNESS = 40  # target value at which or above which a solution is good
GENERATIONS = 100   # number of generations for which a solution to be determined
MUTATION_RATE = 0.5  # rate at which the chromosomes should mutate

# (weight, priority) higher value means heavier or more important
boxes = [(20, 6), (30, 5), (60, 8), (90, 7), (50, 6), (70, 9), (30, 4), (30, 5), (70, 4), (20, 9), (20, 2), (60, 1)]


# initializes a random population
# and returns a unique population with no repeating individuals
def random_population():
    unique_pop_set = set()
    unique_pop_list = []

    while len(unique_pop_set) < POPULATION_SIZE:
        individual = tuple(random.choices([0, 1], k=NUM_BOXES))
        unique_pop_set.add(individual)

    for individual in unique_pop_set:
        new_individual = list(individual)
        unique_pop_list.append(new_individual)

    return list(unique_pop_list)


# fitness function by total value of importance without exceeding the max_weight value
def fitness_function(chromosome):
    total_weight = sum(weight * gene[0] for gene, weight in zip(boxes, chromosome))
    total_importance = sum(importance * gene[1] for gene, importance in zip(boxes, chromosome))

    return total_importance if total_weight <= MAX_WEIGHT else 0


# uses proportion selection to randomly select a parent chromosome
def random_parent_selection(parent_population):
    total_fitness = sum(fitness_function(specie) for specie in parent_population)
    probability = [fitness_function(chromosome) / total_fitness for chromosome in parent_population]

    return parent_population[np.random.choice(len(parent_population), p=probability)]


# single point mutation
def single_point_mutation(chromosome):
    mutant_chromosome = chromosome.copy()
    gene_to_mutate = random.randint(0, len(chromosome) - 1)
    mutant_chromosome[gene_to_mutate] = 1 - mutant_chromosome[gene_to_mutate]

    return mutant_chromosome


# multi-point mutation
def multi_point_mutation(chromosome):
    mutant_chromosome = chromosome.copy()
    genes_to_mutate_num = random.randint(1, len(chromosome))
    while genes_to_mutate_num != 0:
        gene_to_mutate = random.randint(0, len(chromosome) - 1)
        mutant_chromosome[gene_to_mutate] = 1 - mutant_chromosome[gene_to_mutate]
        genes_to_mutate_num -= 1

    return mutant_chromosome


# one point crossover
def one_point_crossover(chromosome_1, chromosome_2):
    crossover_point = random.randint(1, len(chromosome_1) - 1)
    new_chromosome_1 = chromosome_1[:crossover_point] + chromosome_2[crossover_point:]
    new_chromosome_2 = chromosome_2[:crossover_point] + chromosome_1[crossover_point:]

    return new_chromosome_1, new_chromosome_2


# multi point crossover
def multi_point_crossover(chromosome_1, chromosome_2):
    crossover_point_num = random.randint(1, len(chromosome_1))
    new_chromosome_1 = chromosome_1.copy()
    new_chromosome_2 = chromosome_2.copy()
    while crossover_point_num != 0:
        crossover_point = random.randint(1, len(chromosome_1) - 1)
        new_chromosome_1 = chromosome_1[:crossover_point] + chromosome_2[crossover_point:]
        new_chromosome_2 = chromosome_2[:crossover_point] + chromosome_1[crossover_point:]
        crossover_point_num -= 1

    return new_chromosome_1, new_chromosome_2


# population culling function
def population_culling(parent_population):
    sorted_population = sorted(parent_population, key=lambda chromosome: fitness_function(chromosome), reverse=True)
    cull_size = int(len(parent_population) * CULL_PERCENTAGE)

    return sorted_population[:len(parent_population) - cull_size]


# reproduction of new offspring
def reproduce(parent_1, parent_2):
    cross_over_choice = random.randint(0, 1)

    return one_point_crossover(parent_1, parent_2) if cross_over_choice == 0 else \
        (multi_point_crossover(parent_1, parent_2))


# genetic algorithm
def genetic_algorithm(parent_population):
    for generation in range(GENERATIONS):
        new_population = []
        for i in range(POPULATION_SIZE):
            parent_1 = random_parent_selection(parent_population)
            parent_2 = random_parent_selection(parent_population)
            children = reproduce(parent_1, parent_2)
            if random.random() < MUTATION_RATE:
                child_1 = single_point_mutation(children[0]) if random.randint(0, 1) == 0 else \
                    multi_point_mutation(children[0])
                child_2 = single_point_mutation(children[1]) if random.randint(0, 1) == 0 else \
                    multi_point_mutation(children[1])
                new_population.append(child_1)
                new_population.append(child_2)
            else:
                new_population.append(children[0])
                new_population.append(children[1])
            parent_population.extend(new_population)

        parent_population = population_culling(parent_population)

        fitness_values = [fitness_function(chromosome) for chromosome in parent_population]
        high_val_pos = np.argmax(fitness_values)
        best_fitness_val = fitness_values[high_val_pos]

        if best_fitness_val >= TARGET_FITNESS:
            return parent_population[high_val_pos]

    fitness_values = [fitness_function(chromosome) for chromosome in parent_population]
    best_index = np.argmax(fitness_values)
    return parent_population[best_index]


if __name__ == "__main__":
    # initializing a random population
    population = random_population()

    # best individual
    best_individual = genetic_algorithm(population)

    best_arrangement = []
    sum_weight = 0
    sum_value = 0

    for j in range(len(best_individual)):
        if best_individual[j] == 1:
            sum_weight += boxes[j][0]
            sum_value += boxes[j][1]
            best_arrangement.append(boxes[j])

    print("Possible boxes to choose for maximum value: ", best_arrangement)
    print("Total weight of the chosen boxes:", sum_weight)
    print("Total value of the bag:", sum_value)
