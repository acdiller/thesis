"""
Standalone file to ensure that techniques work as expected.
"""
import drawsvg
import random

from eca import ElementaryCA
from circlepack import CirclePacking

test_palette = ["#61E8E1", "#F25757", "#FFC145", "#1F5673"]

def main():
    rng = random.Random()
    rng.seed(22)

    d = drawsvg.Drawing(600, 600)
    sd1 = (0, 0, 300, 300)
    sd2 = (300, 300, 300, 300)

    #e = ElementaryCA(rng, sd2, test_palette)
    #e.draw(d)
    #d.save_svg("test-eca.svg")
    
    cp = CirclePacking(rng, sd1, test_palette)
    
    cp.draw(d)
    #cp2 = CirclePacking(rng, sd2, test_palette, 1, 200, 2)
    #cp2.draw(d)
    d.save_svg("test-circlepack.svg")


if __name__ == "__main__":
    main()