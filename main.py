import argparse
import os
import random
from copy import deepcopy

import shapely

from archive import Archive
from individual import Individual
from pens import pilotV5

from algorithmic_art.techniques import (
    CirclePacking,
    ElementaryCA,
    FlowField,
    Phyllotaxis,
    RadialLines
)

techniques = [CirclePacking, ElementaryCA, FlowField, Phyllotaxis, RadialLines]

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


def createSVG(ind, filename="test.svg"):
    xml_preamble = '<?xml version="1.0" encoding="UTF-8"?>\n'
    w = ind.dim[0]
    h = ind.dim[1]
    svg_root = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"\n \twidth="' + str(w) + '" height="' + str(h) + '" viewBox="0 0 ' + str(w) + ' ' + str(h) + '">\n'
    svg_close = '</svg>'

    all_geoms = []
    for t in ind.techniques:
        all_geoms += t.geoms

    # create random palette from available pen colours
    n_colours = ind.rng.randint(2, 5)
    palette = ind.rng.sample(list(ind.pentype['colours'].keys()), n_colours)
    
    with open(filename, "w") as f:
        f.write(xml_preamble)
        f.write(svg_root)
        for g in all_geoms:
            # create randomized palette from available pen colours
            colour = ind.pentype['colours'][ind.rng.choice(palette)]
            f.write(g.svg(scale_factor=0.5, stroke_color=colour, opacity=1.0) + '\n')
        f.write(svg_close)


def evaluate(ind):
    n_elements = 0
    for t in ind.techniques:
        t.draw()
        n_elements += len(t.geoms)

    ind.features = (len(ind.techniques), n_elements)
    ind.fitness = getOverlaps(ind)


# fitness function - calculates every point of intersection between plot geometries
def getOverlaps(ind):
    print(f"Evaluating {ind.id}")
    all_geoms = []
    for t in ind.techniques:
        all_geoms += t.geoms
    
    shapely.prepare(all_geoms)
    tree = shapely.strtree.STRtree(all_geoms)

    intersections = set()
    for i in range(len(all_geoms)):
        # get indices for anything that intersects with current geom
        indices = tree.query(all_geoms[i], predicate='intersects')
        # calculate specific intersection between current geom and other geoms
        local_intersections = [shapely.intersection(all_geoms[i], all_geoms[oi]) for oi in indices if i < oi]
        
        # filter intersection geometries into individual parts
        for g in local_intersections:
            if isinstance(g, shapely.MultiPoint) or isinstance(g, shapely.MultiLineString):
                intersections.update(g.geoms)   # split MultiPoint or MultiLineString into individual parts
            else:
                intersections.add(g)   # add single Point/LineString/LinearRing 
    
    penwidth = ind.pentype['penwidth']

    mostOverlaps = 0
    for g in intersections:
        # get indices for anything that intersects with the buffered intersection - aka how many things touch at that spot
        indices = tree.query(g.buffer(penwidth/2), predicate='intersects')
        mostOverlaps = max(mostOverlaps, len(indices))
    #print(f"{ind.id} with {mostOverlaps} overlaps")
    
    return mostOverlaps


def mutation(ind, it):
    mutator = deepcopy(ind)
    mutator.id += f"_m{it}"

    # reset geometries, fitness, features, etc.
    for t in mutator.techniques:
        t.reset()
    mutator.features = None
    mutator.fitness = 0.0

    # choose random technique and mutate one of its parameters
    t = mutator.rng.choice(mutator.techniques)
    t.mutate()

    return mutator


# generate random individual
def generate_individual(id, rng, pentype, n_techniques):
    ind = Individual(id, rng, DIM, pentype)
    for _ in range(n_techniques):
            t = rng.choice(techniques)
            ind.techniques.append(t(rng, (0, 0, DIM[0], DIM[1])))
    print(f"Created {ind.id} with techniques: {', '.join(str(t) for t in ind.techniques)}")
    return ind


# randomly generate initial population, evaluate, and add to archive
def initArchive(rng, pop_size, archive):
    for i in range(pop_size):
        id = f"0_{i}"
        n = rng.randrange(archive.fd_bins['n_techniques'][0], archive.fd_bins['n_techniques'][-1])
        ind = generate_individual(id, rng, pilotV5, n)
        evaluate(ind)
        archive.add_to_archive(ind)
        
        
        
def main():
    # cmd-line parameters
    n_iterations = args.iterations
    pop_size = args.population_size
    #xover_rate = args.crossover_rate
    #mut_rate = args.mutation_rate
    
    # create output directory if it doesn't exist
    if not os.path.exists(args.output_path): os.mkdir(args.output_path)
    
    rng = random.Random(args.run_num)

    # techniques
    techniques = [CirclePacking, ElementaryCA, FlowField, Phyllotaxis, RadialLines]

    # configure bins - last element specifies upper bound
    fd_bins = {
        'n_techniques': (2, 3, 4, 5, 6),
        'n_elements': (0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500)
    }

    # initialize archive
    map = Archive(fd_bins)
    print(f"Generating initial population of {pop_size} individuals")
    initArchive(rng, pop_size, map)

    for it in range(1, n_iterations):
        # random selection
        c = rng.choice(list(map.cells))
        x = c[0][2]

        # mutation
        offspring = mutation(x, it)

        # evaluate
        evaluate(offspring)

        map.add_to_archive(offspring)

    print("Elites:")

    for c in map.cells:
        ind = c[0][2]
        print(ind.id, ind.fitness, ind.features[0], ind.features[1])
        createSVG(ind, filename=os.path.join(args.output_path, f"img-{ind.id}.svg"))


if __name__ == "__main__":
    main()