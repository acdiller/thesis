import argparse
import os
import random
from copy import deepcopy

import shapely

import mutation
import pens
import settings
from archive import Archive
from individual import Individual

parser = argparse.ArgumentParser()
parser.add_argument("--run_num", default=0, type=int, help="Run number.")
parser.add_argument("--iterations", default=100, type=int, help="Number of iterations to run MAP-Elites for.")
parser.add_argument("--population_size", default=50, type=int, help="Initial population size.")
#parser.add_argument("--crossover_rate", default=0.4, type=float)
parser.add_argument("--mutation_rate", default=0.01, type=float)
parser.add_argument("--pentype", choices=[pens.pilotV5, pens.pilotV7], default=pens.pilotV5, help="Type of pen to plot with.")
parser.add_argument("--output_path", default="./", type=str, help="Output path.")
args = parser.parse_args()

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
    n_colours = settings.rng.randint(2, 5)
    palette = settings.rng.sample(list(ind.pentype['colours'].keys()), n_colours)
    
    with open(filename, "w") as f:
        f.write(xml_preamble)
        f.write(svg_root)
        for g in all_geoms:
            # create randomized palette from available pen colours
            colour = ind.pentype['colours'][settings.rng.choice(palette)]
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


# generate random individual
def generate_individual(id, n_techniques):
    ind = Individual(id, settings.rng, settings.DIM, settings.pentype)
    for _ in range(n_techniques):
            t = settings.rng.choice(settings.ALL_TECHNIQUES)
            ind.techniques.append(t(settings.rng, (0, 0, settings.DIM[0], settings.DIM[1])))
            #regions = divide_canvas(ind)
            # TODO: assign techniques to regions
    print(f"Created {ind.id} with techniques: {', '.join(str(t) for t in ind.techniques)}")
    return ind


# randomly generate initial population, evaluate, and add to archive
def initArchive(pop_size, archive):
    for i in range(pop_size):
        id = f"0_{i}"
        n = settings.rng.randint(1, settings.MAX_T)
        ind = generate_individual(id, n)
        evaluate(ind)
        archive.add_to_archive(ind)

        
def main():
    # cmd-line arguments
    settings.n_iterations = args.iterations
    settings.pop_size = args.population_size
    #xover_rate = args.crossover_rate
    settings.mutation_rate = args.mutation_rate
    settings.pentype = args.pentype
    
    # create output directory if it doesn't exist
    if not os.path.exists(args.output_path): os.mkdir(args.output_path)
    
    settings.rng = random.Random(args.run_num)

    # configure bins - last element specifies upper bound
    fd_bins = {
        'n_techniques': tuple(range(1, settings.MAX_T)),
        'n_elements': tuple(range(0, settings.MAX_ELEM+1, settings.ELEM_STEP))
    }

    # initialize archive
    map = Archive(fd_bins)
    print(f"Generating initial population of {settings.pop_size} individuals")
    initArchive(settings.pop_size, map)

    for it in range(1, settings.n_iterations):
        # random selection
        c = settings.rng.choice(list(map.cells))
        x = c[0][2]

        # mutation
        offspring = mutation.apply_mutation(x, it)

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