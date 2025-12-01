"""
Standalone file to ensure that techniques/tools work as expected.
"""
import random

import shapely

from algorithmic_art.techniques import (
    CirclePacking,
    ElementaryCA,
    FlowField,
    LineTiles,
    Phyllotaxis,
    RadialLines
)

from algorithmic_art.tools.shapes import hexagon, rect, circular_sinewave

DIM = (1054, 816)   # US letter paper at 96 DPI
#test_palette = ["#61E8E1", "#F25757", "#FFC145", "#1F5673"]
test_palette = ["#FC0FC0", "#FF7F00", "#FFFF00", "#32CD32", "#0FC0FC"]

def createSVG(ind=None, elems=None, filename="test.svg"):
    xml_preamble = '<?xml version="1.0" encoding="UTF-8"?>\n'
    w = DIM[0]
    h = DIM[1]
    svg_root = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n \twidth="' + str(w) + '" height="' + str(h) + '" viewBox="0 0 ' + str(w) + ' ' + str(h) + '">\n'
    svg_close = '</svg>'

    geoms = None
    if ind is not None:
        geoms = ind.geoms
    else:
        geoms = elems

    geoms = shapely.set_precision(geoms, 0.001)
    #geoms.append(rect(0, 0, w, h))
        
    with open(filename, "w") as f:
        f.write(xml_preamble)
        f.write(svg_root)
        for g in geoms:
            colour = random.choice(test_palette)
            f.write(g.svg(scale_factor=0.5, stroke_color=colour, opacity=1.0) + '\n')
        f.write(svg_close)


def main():
    rng = random.Random()
    rng.seed(22)

    sd = (0, 0, DIM[0], DIM[1])
    #sd = (DIM[0]/2, DIM[1]/2, DIM[0], DIM[1])

    ff = FlowField(rng, sd, style='flowy')
    ff.draw()
    #ff.geoms = shapely.simplify(ff.geoms, tolerance=0.1)
    createSVG(ff, filename="ff-simplified-test.svg")

    #e = ElementaryCA(rng, sd, init_state="random", rule=30, cellsize=10)
    #e.mutate()
    #e.draw()
    #createSVG(e, filename="eca-test.svg")
    
    #cp = CirclePacking(rng, sd, shape_type="sinewave")
    #cp.mutate()
    #cp.draw()
    #cp.geoms = shapely.simplify(cp.geoms, tolerance=0.2, preserve_topology=False)
    #createSVG(cp, filename="cp-sinewave-test.svg")

    r = 25
    freq = 10
    amp = 2

    #csw = circular_sinewave(50, 50, r, freq, amp)

    #print("csw", shapely.get_num_points(csw))
    #createSVG(elems=[csw], filename="csw-test.svg")

    #phy = Phyllotaxis(rng, sd, n, c, mod, radius, freq, amp)
    #phy.draw()
    #createSVG(phy, filename="phy-test.svg")

    #h = hexagon(100, 100, 100)
    #createSVG(elems=[h])

    #rad = RadialLines(rng, sd)
    #rad.draw()
    #createSVG(rad, filename="radial-lines-test.svg")
    #print(rad)

    #lt = LineTiles(rng, sd, step=5.0, noise_based=False)
    #lt.draw()
    #createSVG(lt, filename="linetiles-test.svg")
    



if __name__ == "__main__":
    main()
