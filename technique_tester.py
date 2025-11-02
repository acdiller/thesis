"""
Standalone file to ensure that techniques work as expected.
"""
import random

from algorithmic_art import *

test_palette = ["#61E8E1", "#F25757", "#FFC145", "#1F5673"]

def createSVG(ind):
    xml_preamble = '<?xml version="1.0" encoding="UTF-8"?>\n'
    w = ind.width
    h = ind.height
    svg_root = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n \twidth="' + str(w) + '" height="' + str(h) + '" viewBox="0 0 ' + str(w) + ' ' + str(h) + '">\n'
    svg_close = '</svg>'
    
    geoms = ind.geoms
    # TODO: devise specific filenaming pattern
    filename = "ff-test.svg"
    
    with open(filename, "w") as f:
        f.write(xml_preamble)
        f.write(svg_root)
        for g in geoms:
            # TODO: color assignment
            colour = random.choice(test_palette)
            f.write(g.svg(scale_factor=0.5, stroke_color=colour, opacity=1.0) + '\n')
        f.write(svg_close)


def main():
    rng = random.Random()
    rng.seed(12)

    DIM = (800, 800)

    sd = (0, 0, DIM[0], DIM[1])

    ff = FlowField(rng, sd, style='flowy')
    ff.draw()
    createSVG(ff)
    print(ff)

    #e = ElementaryCA(rng, sd)
    #print(e)
    #e.mutate()
    #e.draw()
    
    #cp = CirclePacking(rng, sd)
    #print(cp)
    #cp.mutate()
    #cp.draw()


if __name__ == "__main__":
    main()