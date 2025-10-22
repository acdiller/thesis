import argparse
import itertools
import os
import random
import shapely

from copy import deepcopy
from drawsvg import Drawing

from archive import Archive
from individual import Individual
from techniques import CirclePacking, ElementaryCA
from time import perf_counter

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
    n_elements = 0
    for t in ind.techniques:
        t.draw(ind.drawing)
        n_elements += len(t.geoms)

    ind.features = (len(ind.techniques), n_elements)
    ind.isEvaluated = True


# fitness function - calculates every point of intersection between plot geometries
def getOverlaps(ind):
    all_geoms = []
    for t in ind.techniques:
        all_geoms += t.geoms
    
    shapely.prepare(all_geoms)
    tree = shapely.strtree.STRtree(all_geoms)

    intersections = []
    for i in range(len(all_geoms)):
        indices = tree.query(all_geoms[i], predicate='intersects')
        local_intersections = [shapely.intersection(all_geoms[i], all_geoms[oi]) for oi in indices if i < oi]
        for i in local_intersections:
            if i.geom_type == 'Point':
                intersections.append(i)
            else:
                intersections += i.geoms    # split MultiPoint into individual Points
    
    # TODO: how many points fall in a given spot?




def mutation(ind):
    pass


def generateIndividual(rng, all_techniques):
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
def initArchive(rng, pop_size, archive, all_techniques):
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
    test_ind = generateIndividual(shared_rng, techniques)

    behaviour = evaluate(test_ind)
    print(behaviour)

    test_ind.drawing.save_svg("test-individual.svg")


if __name__ == "__main__":
    #main()
    rng = random.Random(22)
    techniques = [CirclePacking, ElementaryCA]

    test_ind = generateIndividual(rng, techniques)
    evaluate(test_ind)

    #test_ind.drawing.save_svg("test-individual.svg")
    print("number of techniques: " + str(test_ind.features[0]))
    print("number of elements: " + str(test_ind.features[1]))

    start = perf_counter()
    n_intersections = getOverlaps(test_ind)
    end = perf_counter()
    
    coords = shapely.get_coordinates(n_intersections).tolist()
    print("number of intersections: " + str(len(coords)))
    print("time to find intersections: " + str(end-start) + "s")