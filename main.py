import argparse
import os
import random

from copy import deepcopy
from individual import Individual
from plotter import penplot
from techniques.flowfield import FlowField

parser = argparse.ArgumentParser()
parser.add_argument("--generations", default=25, type=int)
parser.add_argument("--population_size", default=50, type=int)
#parser.add_argument("--crossover_rate", default=0.4, type=float)
parser.add_argument("--mutation_rate", default=0.2, type=float)
parser.add_argument("--output_path", default="./", type=str)
args = parser.parse_args()


# draw out algorithmic technique, run plot simulation
def evaluate(ind):
    # draw
    ind.technique.draw(ind.drawing)
    plot_svg = ind.drawing.as_svg()
    ind.plot_info = penplot.simulate_plot(plot_svg)
    ind.isEvaluated = True
    #return ind


# generate random initial population
def init_population(pop_size, rng, dim, pal):
    pop = []
    print(f"Generating initial population of {pop_size}")
    for i in range(pop_size):
        res = rng.randint(2, 6)
        ns = rng.randrange(100, 800)
        octaves = rng.randrange(2, 26)
        id = f"0_{i}"
        pop.append(Individual(id, dim, rng, FlowField(rng, pal, res, ns, octaves)))
    return pop


# TODO: calculate actual fitness value, using dist_drawn as stand-in
def fitness_function(ind):
    ind.fitness = ind.plot_info["dist_drawn"]


def mutation(ind):
    mutator = deepcopy(ind)
    #mutator.id += f"_m_{


def main():
    # cmd-line parameters
    num_gens = args.generations
    pop_size = args.population_size
    mut_rate = args.mutation_rate

    # create output directory if it doesn't exist
    if not os.path.exists(args.output_path): os.mkdir(args.output_path)

    # configure bins
    ns_bins = [100, 200, 300, 400, 500, 600, 700, 800]  # noise scale
    oct_bins = [2, 6, 10, 14, 18, 22, 26]   # noise detail - octaves

    # seed rng & noise
    rng = random.Random()
    rng.seed(22)

    # initialize archive
    archive = {}

    dim = (500, 500)
    pal = ["#28AFB0"]   # single colour palette for testing
    # generate initial population
    population = init_population(pop_size, rng, dim, pal)

    # initial evaluation
    for ind in population:
        evaluate(ind)
        fitness_function(ind)

        b = (ind.technique.noisescale, ind.technique.octaves)

        # determine index for corresponding cell in archive
        ns_i = None
        oct_i = None
        for i in range(len(ns_bins)-1):
            if (b[0] >= ns_bins[i]) and (b[0] < ns_bins[i+1]):
                ns_i = i
                break
        
        for i in range(len(oct_bins)-1):
            if (b[1] >= oct_bins[i]) and (b[1] < oct_bins[i+1]):
                oct_i = i
                break
        
        # add to archive
        #if ((ns_i, oct_i) not in archive) or archive[(ns_i, oct_i)].fitness < ind.fitness:
        if (ns_i, oct_i) not in archive:
            archive[(ns_i, oct_i)] = ind
            print(f"{ind.id}, fitness: {ind.fitness}, placed at {(ns_i, oct_i)}")
        elif archive[(ns_i, oct_i)].fitness < ind.fitness:
            print(f"{archive[(ns_i, oct_i)].id}, fitness: {archive[(ns_i, oct_i)].fitness} replaced by {ind.id}, fitness: {ind.fitness} at {(ns_i, oct_i)}")


    #for gen in range(1, num_gens):
        # selection

        # mutation

        # evaluate

        # grid placement
    
    # get elites
    elites = archive.values()
    
    # save SVGs for elites
    for ind in elites:
        ind.drawing.save_svg(os.path.join(args.output_path, f"img-{ind.id}.svg"))


if __name__ == "__main__":
    main()