import argparse
import os
import random

from copy import deepcopy
from drawsvg import Drawing

from archive import Archive
from individual import Individual
from techniques import CirclePacking, ElementaryCA
#from plotter import penplot

parser = argparse.ArgumentParser()
parser.add_argument("--run_num", default=0, type=int, help="Run number.")
parser.add_argument("--iterations", default=100, type=int, help="Number of iterations to run MAP-Elites for.")
parser.add_argument("--population_size", default=50, type=int, help="Initial population size.")
#parser.add_argument("--crossover_rate", default=0.4, type=float)
#parser.add_argument("--mutation_rate", default=0.2, type=float)
parser.add_argument("--overlap", action="store_true", default=False, help="Whether to overlap or partition techniques.")
parser.add_argument("--output_path", default="./", type=str, help="Output path.")
args = parser.parse_args()


DIM = (1054, 816)   # US letter paper at 96 DPI
test_palette = ["#61E8E1", "#F25757", "#FFC145", "#1F5673"]


def evaluate(ind):
    num_elements = 0
    for t in ind.techniques:
        t.draw(ind.drawing)
        num_elements += len(t.geoms)

    ind.isEvaluated = True
    return (len(ind.techniques), num_elements)


def fitness_function(ind):
    pass


def mutation(ind):
    pass


def init_individual(rng, all_techniques):
    d = Drawing(DIM[0], DIM[1])
    
    #num_tech = rng.randint(2, 6)
    num_tech = 2
    
    ind_techniques = []

    for _ in range(num_tech):
        t = rng.choice(all_techniques)
        tech = t(rng, (0, 0, DIM[0], DIM[1]), test_palette)
        ind_techniques.append(tech)
    
    ind = Individual(1, rng, DIM, d, ind_techniques)
    
    return ind


def partition_canvas(dim, num_techniques):
    w = dim[0]
    h = dim[1]
    
    if num_techniques == 2:
        return [(0, 0, w/2, h), (w/2, 0, w, h)]
    elif num_techniques == 3:
        return [(0, 0, w/3, h),
                (w/3, 0, w-w/3, h),
                (w-w/3, 0, w, h)]
    elif num_techniques == 4:
        return [(0, 0, w/2, h/2),
                (w/2, 0, w, h/2),
                (0, h/2, w/2, h),
                (w/2, h/2, w, h)]
                 

# TODO: determine palettes
# create random initial population and add to archive
def init_archive(rng, pop_size, archive, all_techniques):
    for i in range(pop_size):
        id = f"0_{i}"
        d = Drawing(DIM[0], DIM[1])

        num_tech = rng.randint(2, 6)
        ind_techniques = []



        


def main():
    # cmd-line parameters
    num_iterations = args.iterations
    pop_size = args.population_size
    #xover_rate = args.crossover_rate
    #mut_rate = args.mutation_rate
    
    # create output directory if it doesn't exist
    #if not os.path.exists(args.output_path): os.mkdir(args.output_path)
    
    shared_rng = random.Random(args.run_num)

    # techniques
    techniques = [CirclePacking, ElementaryCA]

    # configure bins - last element specifies upper bound
    fd_bins = {
        'num_techniques': (2, 3, 4, 5, 6, 7),
        'num_elements': (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100)
    }

    # initialize archive
    archive = Archive(fd_bins)

    #init_archive(shared_rng, pop_size, archive, techniques)
    test_ind = init_individual(shared_rng, techniques)

    behaviour = evaluate(test_ind)
    print(behaviour)

    test_ind.drawing.save_svg("test-individual.svg")


if __name__ == "__main__":
    #main()
    w = DIM[0]
    h = DIM[1]

    sd1 = (0, 0, w/2, h/2)
    sd2 = (w/2, 0, w, h/2)
    sd3 = (0, h/2, w/2, h)
    sd4 = (w/2, h/2, w, h)

    rng = random.Random(22)

    cp1 = CirclePacking(rng, sd1, test_palette)
    eca1 = ElementaryCA(rng, sd2, test_palette)
    cp2 = CirclePacking(rng, sd4, test_palette)
    eca2 = ElementaryCA(rng, sd3, test_palette)

    d = Drawing(DIM[0], DIM[1])

    test_ind = Individual(1, rng, DIM, d, [cp1, eca1, eca2, cp2])

    for t in test_ind.techniques:
        t.draw(test_ind.drawing)
    
    test_ind.drawing.save_svg("partitioned-test-ind.svg")

