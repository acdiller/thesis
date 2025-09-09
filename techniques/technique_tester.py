"""
Standalone file to ensure that techniques work as expected.
"""
import drawsvg
import random

from eca import ElementaryCA

test_palette = ["#61E8E1", "#F25757", "#FFC145", "#1F5673"]

def main():
    rng = random.Random()
    rng.seed(22)

    d = drawsvg.Drawing(600, 600)
    sd1 = (0, 0, 300, 300)
    sd2 = (300, 300, 300, 300)

    e = ElementaryCA(rng, sd1, test_palette, 20)
    e.draw(d)
    e2 = ElementaryCA(rng, sd2, test_palette, 40)
    e2.draw(d)
    d.save_svg("test-eca.svg")


if __name__ == "__main__":
    main()