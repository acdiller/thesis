"""
Standalone file to ensure that techniques/tools work as expected.
"""
import random

import shapely

import settings

from algorithmic_art.techniques import (
    CirclePacking,
    ElementaryCA,
    FlowField,
    LineTiles,
    Phyllotaxis,
    RadialLines
)

from algorithmic_art.tools.shapes import (
    circle,
    circular_sinewave,
    hexagon,
    rect
)

test_palette = ["#054A91", "#62BFED", "#C81D25", "#A0C940"]

def createSVG(ind=None, elems=None, filename="test.svg"):
    xml_preamble = '<?xml version="1.0" encoding="UTF-8"?>\n'
    w = settings.DIM[0]
    h = settings.DIM[1]
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
            if isinstance(g, shapely.Point):
                f.write(g.svg(scale_factor=0.5, fill_color=colour, opacity=1.0) + '\n')
            elif isinstance(g, shapely.Polygon):
                f.write(poly_to_svg(g, scale_factor=0.5, fill_color=colour) + '\n')
            else:
                f.write(g.svg(scale_factor=0.5, stroke_color=colour, opacity=1.0) + '\n')
        f.write(svg_close)


def poly_to_svg(geom, scale_factor, fill_color, stroke_color=None, opacity=1.0):
    if geom.is_empty:
        return "<g />"
    if stroke_color is None:
        stroke_color = fill_color
    exterior_coords = [["{},{}".format(*c) for c in geom.exterior.coords]]
    interior_coords = [
        ["{},{}".format(*c) for c in interior.coords] for interior in geom.interiors
    ]
    path = " ".join(
        [
            "M {} L {} z".format(coords[0], " L ".join(coords[1:]))
            for coords in exterior_coords + interior_coords
        ]
    )
    return (
        f'<path fill-rule="evenodd" fill="{fill_color}" stroke="{stroke_color}" '
        f'stroke-width="{2.0 * scale_factor}" opacity="{opacity}" d="{path}" />'
    )


def circlepack(rng, sd, output_svg=True):
    
    cp = CirclePacking(rng, sd, shape_type='circle', n_spawn=1, start_r=15, max_failures=50, pad=5)
    #cp.mutate()
    cp.draw()
    #cp.geoms = shapely.simplify(cp.geoms, tolerance=0.2, preserve_topology=False)
    
    if output_svg:
        createSVG(cp, filename="cp-sinewave-test.svg")
    else:
        return cp


def elemca(rng, sd=None, output_svg=True):
    eca = ElementaryCA(rng, sd, init_state="random", rule=30, cellsize=10)
    #eca.mutate()
    eca.draw()
    
    if output_svg:
        createSVG(eca, filename="eca-test.svg")
    else:
        return eca


def flowfield(rng, sd=None, output_svg=True):
    res = 4
    ns = 800
    octs = 8
    pers = 0.25
    lac = 2.0
    
    #ff = FlowField(rng, sd, style='flowy', resolution=res, noisescale=ns, octaves=octs, persistence=pers, lacunarity=lac)
    ff = FlowField(rng, sd, style='flowy')
    ff.draw()
    #ff.geoms = shapely.simplify(ff.geoms, tolerance=0.1)

    if output_svg:
        createSVG(ff, filename="ff-test.svg")
    else:
        return ff
    

def linetiles(rng, sd=None, output_svg=True):
    lt = LineTiles(rng, subdim=sd, noise_based=False)
    lt.draw()

    if output_svg:
        createSVG(lt, filename="linetiles-test.svg")
    else:
        return lt
    

def phyllo(rng, sd=None, output_svg=True):
    n = 75
    c = 10
    mod = 5
    radius = 40
    freq = 10
    amp = 4
    
    phy = Phyllotaxis(rng, sd, n, c, mod, radius, freq, amp)
    phy.draw()

    if output_svg:
        createSVG(phy, filename="phyllotaxis-test.svg")
    else:
        return phy


def radlines(rng, sd=None, output_svg=True):
    rad = RadialLines(rng, sd)
    rad.draw()
    
    if output_svg:
        createSVG(rad, filename="radlines-test.svg")
    else:
        return rad


def cropped(rng, sd=None):
    ff = flowfield(rng, sd, output_svg=False)
    cp = circlepack(rng, sd, output_svg=False)

    croples = [shapely.Polygon(c) for c in cp.geoms]
    croples = shapely.MultiPolygon(croples)
    cropped_ff = shapely.intersection(ff.geoms, croples).tolist()
    
    #cropped_ff += shapely.boundary(cp.geoms).tolist()

    createSVG(elems=cropped_ff, filename="cropped-ff-test.svg")


def main():
    rng = random.Random()
    rng.seed(22)

    #csw = circular_sinewave(50, 50, r=25, freq=10, amp=2)
    #print("csw", shapely.get_num_points(csw))
    #createSVG(elems=[csw], filename="csw-filled-test.svg")

    # cp = CirclePacking(rng)
    # cp.draw()
    # eca = ElementaryCA(rng)
    # eca.draw()
    # stuff = cp.geoms + eca.geoms
    # createSVG(elems=stuff, filename="cp-eca-filled-test.svg")

    linetiles(rng)


if __name__ == "__main__":
    main()
