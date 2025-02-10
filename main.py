import random
import argparse
from individual import Individual
from techniques.flowfield import FlowField

parser = argparse.ArgumentParser()
parser.add_argument('--generations', default=25, type=int)
parser.add_argument('--population_size', default=50, type=int)
#parser.add_argument('--crossover_rate', default=0.4, type=float)
parser.add_argument('--mutation_rate', default=0.2, type=float)
args = parser.parse_args()


def evaluate(ind):
    # draw
    t = ind.technique
    ind.drawing = t.draw(ind.drawing)
    ind.isEvaluated = True
    #return ind


# need tidier way to generate individuals
def generate_population(pop_size, rng, dim, pal):
    pop = []
    for i in range(pop_size):
        res = rng.randint(2, 6)
        ns = rng.randint(100, 800)
        oct = rng.randint(2, 24)
        ff = FlowField(rng, pal, res, ns, oct)
        pop.append(Individual(i, dim, rng, ff))
    return pop


# TODO: run plot estimate, get time/dist drawn
def fitness_function(ind):
    pass


#TODO: figure out whatever this is
def mutation():
    pass


if __name__ == "__main__":
    # cmd-line parameters
    num_gens = args.generations
    pop_size = args.population_size
    mut_rate = args.mutation_rate

    # TODO: output dir

    # configure bins
    ns_bins = []
    oct_bins = []

    # seed rng & noise
    rng = random.Random()
    rng.seed(22)

    # initialize grid archive
    archive = [[None for _ in range(len(ns_bins))] for _ in range(len(oct_bins))]

    dim = (500, 500)
    pal = ["#28AFB0"]   # single colour palette for testing
    # generate initial population
    population = generate_population(pop_size, rng, dim, pal)

    # initial evaluation
    for ind in population:
        evaluate(ind)
        #ind.fitness = fitness_function(ind)

        # determine corresponding cell in archive
        ns_index = None
        oct_index = None

        #TODO: need to check the actual correct parameters and not the dummy ones
        for i, bin in enumerate(ns_bins):
            if (ind.p1 >= bin[0]) and (ind.p1 <= bin[1]):
                ns_index = i
                break
        
        for i, bin in enumerate(oct_bins):
            if (ind.p2 >= bin[0]) and (ind.p2 <= bin[1]):
                oct_index = i
                break


    #for gen in range(1, num_gens):
        # selection

        # mutation

        # evaluate

        # grid placement