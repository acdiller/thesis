"""
Standalone file to ensure that techniques/tools work as expected.
"""
import random

from algorithmic_art.techniques import (
    CirclePacking,
    ElementaryCA,
    FlowField,
    Phyllotaxis,
    RadialLines
)

from algorithmic_art.tools.shapes import hexagon, rect

DIM = (1054, 816)   # US letter paper at 96 DPI
test_palette = ["#61E8E1", "#F25757", "#FFC145", "#1F5673"]

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

    sd = (0, 0, DIM[0], DIM[1])
    #sd = (DIM[0]/2, DIM[1]/2, DIM[0], DIM[1])

    #ff = FlowField(rng, sd, style='flowy')
    #ff.draw()
    #createSVG(ff)
    #print(ff)

    #e = ElementaryCA(rng, sd)
    #e.mutate()
    #e.draw()
    #createSVG(e, filename="eca-test.svg")
    
    #cp = CirclePacking(rng, sd, shape_type="sinewave")
    #cp.mutate()
    #cp.draw()
    #createSVG(cp, filename="cp-sinewave-test.svg")

    n = 200
    c = 10
    mod = 5
    radius = 70
    freq = 12
    amp = 4

    #phy = Phyllotaxis(rng, sd, n, c, mod, radius, freq, amp)
    #phy.draw()
    #createSVG(phy, filename="phy-test.svg")

    #h = hexagon(100, 100, 100)
    #createSVG(elems=[h])

    rad = RadialLines(rng, sd)
    rad.draw()
    createSVG(rad, filename="radial-lines-test.svg")
    print(rad)
    



if __name__ == "__main__":
    main()
