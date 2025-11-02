import shapely
import numpy as np
import math

w = 600
h = 600

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

def createSVG(geoms):
    xml_preamble = '<?xml version="1.0" encoding="UTF-8"?>\n'

    svg_root = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n \twidth="' + str(w) + '" height="' + str(h) + '" viewBox="0 0 ' + str(w) + ' ' + str(h) + '">\n'
    svg_close = '</svg>'
    
    filename = "curve-test.svg"
    
    with open(filename, "w") as f:
        f.write(xml_preamble)
        f.write(svg_root)
        for g in geoms:
            if isinstance(g, shapely.Point):
                f.write(g.svg(scale_factor=0.5, fill_color='#FF0000', opacity=1.0) + '\n')
            else:
                f.write(g.svg(scale_factor=0.5, stroke_color='#FF0000', opacity=1.0) + '\n')
        f.write(svg_close)


def lerp(start, stop, amt):
    return amt * (stop-start) + start


def quadString(p0, p1, p2, delta=0.1):
    lines = []

    for t in np.linspace(0, 1, int(1/delta)):
        x1 = lerp(p0.x, p1.x, round(t, 1))
        y1 = lerp(p0.y, p1.y, round(t, 1))

        x2 = lerp(p1.x, p2.x, round(t, 1))
        y2 = lerp(p1.y, p2.y, round(t, 1))
        
        lines.append(shapely.LineString([[x1, y1], [x2, y2]]))

    return lines


def cubicString(p0, p1, p2, p3, delta=0.1):
    lines = []

    for t in np.linspace(0, 1, int(1/delta)):
        v1 = quadratic(p0, p1, p2, t)
        v2 = quadratic(p1, p2, p3, t)
        x = lerp(v1.x, v2.x, t)
        y = lerp(v1.y, v2.y, t)
        
        lines.append(shapely.LineString([[v1.x, v1.y], [v2.x, v2.y]]))

    return lines


def quadratic(p0, p1, p2, t):
    x1 = lerp(p0.x, p1.x, round(t, 1))
    y1 = lerp(p0.y, p1.y, round(t, 1))

    x2 = lerp(p1.x, p2.x, round(t, 1))
    y2 = lerp(p1.y, p2.y, round(t, 1))

    x = lerp(x1, x2, t)
    y = lerp(y1, y2, t)

    return Vector(x, y)


def cubic(p0, p1, p2, p3, t):
    v1 = quadratic(p0, p1, p2, t)
    v2 = quadratic(p1, p2, p3, t)
    x = lerp(v1.x, v2.x, t)
    y = lerp(v1.y, v2.y, t)

    return Vector(x, y)


def main():
    delta = 0.1
    # quadratic
    #p0 = Vector(0, 300)
    #p1 = Vector(300, 0)
    #p2 = Vector(600, 300)

    # cubic
    p0 = Vector(0, 300)     # first anchor
    p1 = Vector(300, 100)     # first control
    p2 = Vector(400, 500)     # second control
    p3 = Vector(600, 300)   # second anchor

    geoms = []
    
    #c = quadBezier(p0, p1, p2, delta=0.02)
    #geoms.append(c)
    coords = []
    for t in np.linspace(0, 1, int(1/delta)+1):
        #p = quadratic(p0, p1, p3, t)
        p = cubic(p0, p1, p2, p3, t)
        
        coords.append((p.x, p.y))

    curve = shapely.LineString(coords)
    #l = cubicString(p0, p1, p2, p3)
    #l.append(curve)

    createSVG([curve])


if __name__ == '__main__':
    main()