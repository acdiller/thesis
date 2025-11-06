"""
Standalone file to ensure that techniques/tools work as expected.
"""
import random

from algorithmic_art.techniques import (
    CirclePacking,
    ElementaryCA,
    FlowField,
    Phyllotaxis
)

from algorithmic_art.tools.shapes import hexagon

DIM = (800, 800)
test_palette = ["#61E8E1", "#F25757", "#FFC145", "#1F5673"]

def createSVG(ind, filename="test.svg"):
    xml_preamble = '<?xml version="1.0" encoding="UTF-8"?>\n'
    w = DIM[0]
    h = DIM[1]
    svg_root = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n \twidth="' + str(w) + '" height="' + str(h) + '" viewBox="0 0 ' + str(w) + ' ' + str(h) + '">\n'
    svg_close = '</svg>'
    
    with open(filename, "w") as f:
        f.write(xml_preamble)
        f.write(svg_root)
        for g in ind.geoms:
            # TODO: color assignment
            colour = random.choice(test_palette)
            f.write(g.svg(scale_factor=0.5, stroke_color=colour, opacity=1.0) + '\n')
        f.write(svg_close)


def main():
    rng = random.Random()
    rng.seed(12)

    DIM = (800, 800)

    sd = (0, 0, DIM[0], DIM[1])

    #ff = FlowField(rng, sd, style='flowy')
    #ff.draw()
    #createSVG(ff)
    #print(ff)

    #e = ElementaryCA(rng, sd)
    #print(e)
    #e.mutate()
    #e.draw()
    
    cp = CirclePacking(rng, sd)
    #print(cp)
    #cp.mutate()
    cp.draw()
    createSVG(cp, filename="cp-test.svg")

    n = 200
    c = 10
    mod = 5
    radius = 70
    freq = 12
    amp = 4

    #phy = Phyllotaxis(rng, sd, n, c, mod, radius, freq, amp)
    #phy.draw()
    #createSVG(phy, filename="phy-test.svg")



if __name__ == "__main__":
    main()