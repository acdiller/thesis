"""
Shape creation using Shapely geometries.

Note: closed shapes (e.g., circles, rectangles) produce a LineString 
representing the boundary (outline/stroke) of the geometry.
"""
import math

import shapely

from algorithmic_art.tools.curves import catrom_curve


def circle(cx, cy, r, filled=False):
    """
    Create a circle centered at (cx, cy).

    Args:
        cx (int or float): x-coordinate of the centerpoint
        cy (int or float): y-coordinate of the centerpoint
        r (int or float): radius of the circle
    
    Returns:
        shapely.LineString: outline of the circle
    """
    if filled:
        return shapely.Point(cx, cy).buffer(r)
    else:
        return shapely.Point(cx, cy).buffer(r).boundary


def rect(x, y, w, h, filled=False):
    """
    Create a rectangle with its top-left corner at (x, y).

    Args:
        x (int or float): x-coordinate of the top-left corner
        y (int or float): y-coordinate of the top-left corner
        w (int or float): width of the rectangle
        h (int or float): height of the rectangle
    
    Returns:
        shapely.LineString: outline of the rectangle (filled=False)
        shapely.Polgyon: rectangle (filled=True)
    """
    x2 = x + w
    y2 = y + h
    if filled:
        return shapely.box(x, y, x2, y2)
    else:
        return shapely.box(x, y, x2, y2).boundary


def hexagon(cx, cy, r, filled=False):
    """
    Create a hexagon centered at (cx, cy).

    Args:
        cx (int or float): x-coordinate of the centerpoint
        cy (int or float): y-coordinate of the centerpoint
        r (int or float): circumradius
    
    Returns:
        shapely.LineString: outline of the hexagon (filled=False)
        shapely.Polygon: filled-in hexagon (filled=True)
    """
    hexpoints = []
    for a in range(0, 360, 60):
        cx += math.cos(math.radians(a)) * r
        cy += math.sin(math.radians(a)) * r
        hexpoints.append(shapely.Point(cx, cy))
    hexpoints.append(hexpoints[0])  # add first vertex again to close shape
    if filled:
        return shapely.Polygon(hexpoints)
    else:
        return shapely.LineString(hexpoints)


def circular_sinewave(cx, cy, r, freq, amp, filled=False):
    a = 0
    step = 0.075

    dx = cx + (r + math.sin(a * freq) * amp) * math.cos(a)
    dy = cy + (r + math.sin(a * freq) * amp) * math.sin(a)
    
    # calculate points to interpolate curve through
    base_points = [shapely.Point(dx, dy)]   # first control point
    while a < math.pi * 2:
        dx = cx + (r + math.sin(a * freq) * amp) * math.cos(a)
        dy = cy + (r + math.sin(a * freq) * amp) * math.sin(a)

        base_points.append(shapely.Point(dx, dy))

        a += step
    base_points.append(shapely.Point(dx, dy))  # last control point
    curve_points = catrom_curve(base_points, res=0.75)
    
    if filled:
        return shapely.Polygon(shapely.LinearRing(curve_points))
    else:
        return shapely.LinearRing(curve_points)