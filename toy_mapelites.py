import math
import random
import argparse
from individual import Individual

#parser = argparse.ArgumentParser()
#parser.add_argument('--generations', default=25, type=int)
#parser.add_argument('--population_size', default=50, type=int)
#parser.add_argument('--crossover_rate', default=0.4, type=float)
#parser.add_argument('--mutation_rate', default=0.2, type=float)
#args = parser.parse_args()

rng = random.Random()
rng.seed(22)


def evaluate(ind):
    pass


def generate_population(pop_size):
    pop = []
    for i in range(pop_size):
        pop.append(Individual(i, rng.randint(1, 16), rng.randint(1, 12)))
    return pop


def fitness_function(ind):
    return ind.p1 + ind.p2
    

def behaviour(ind):
    pass


if __name__ == "__main__":
    #num_gens = args.generations
    #pop_size = args.population_size
    num_gens = 10
    pop_size = 20

    bins1 = [(1, 4), (5, 8), (9, 12), (13, 16)]
    bins2 = [(1, 4), (5, 8), (9, 12)]
    #bin_list = [bins1, bins2]

    # init grid
    grid = [[None for _ in range(len(bins1))] for _ in range(len(bins2))]



    population = generate_population(pop_size)

    for ind in population:
        ind.fitness = fitness_function(ind)
        #ind['behaviour'] = behaviour(ind)

        # determine what bin an individual falls into for each feature
        b1_index = None
        b2_index = None

        for i, bin in enumerate(bins1):
            if (ind.p1 >= bin[0]) and (ind.p1 <= bin[1]):
                b1_index = i
                break
        
        for i, bin in enumerate(bins2):
            if (ind.p2 >= bin[0]) and (ind.p2 <= bin[1]):
                b2_index = i
                break
        
        # if cell is empty or ind fitness is higher than current occupant
        if (not grid[b2_index][b1_index]) or (grid[b2_index][b1_index].fitness < ind.fitness):
            grid[b2_index][b1_index] = ind
        
    for row in grid:
        print(*row)

