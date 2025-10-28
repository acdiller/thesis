"""
Standalone file to ensure that techniques work as expected.
"""
import drawsvg
import random

from .eca import ElementaryCA
from .circlepack import CirclePacking
from .flowfield import FlowField

test_palette = ["#61E8E1", "#F25757", "#FFC145", "#1F5673"]

def createSVG(ind):
    xml_preamble = '<?xml version="1.0" encoding="UTF-8"?>\n'
    w = ind.width
    h = ind.height
    svg_root = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"\n \twidth="' + str(w) + '" height="' + str(h) + '" viewBox="0 0 ' + str(w) + ' ' + str(h) + '">\n'
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

    d = drawsvg.Drawing(600, 600)

    sd1 = (0, 0, 300, 300)
    sd2 = (300, 300, 600, 600)

    ff = FlowField(rng, (0, 0, 500, 500), test_palette)
    ff.draw(d)
    createSVG(ff)

    #e = ElementaryCA(rng, sd2, test_palette)
    #e.mutate()
    #e.draw(d)
    #d.save_svg("test-eca-mutated.svg")
    
    #cp = CirclePacking(rng, sd1, test_palette)
    #cp.mutate()

    #cp.draw(d)
    #d.save_svg("test-circlepack-mutated.svg")


if __name__ == "__main__":
    main()