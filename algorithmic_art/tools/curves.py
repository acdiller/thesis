"""
Quadratic Bezier, cubic Bezier, and Catmull-Rom splines.
"""
import numpy as np
from shapely import Point

from algorithmic_art.tools.art_utils import lerp


def _quad_lerp(p0, p1, p2, t):
    x1 = lerp(p0.x, p1.x, round(t, 1))
    y1 = lerp(p0.y, p1.y, round(t, 1))

    x2 = lerp(p1.x, p2.x, round(t, 1))
    y2 = lerp(p1.y, p2.y, round(t, 1))

    x = lerp(x1, x2, t)
    y = lerp(y1, y2, t)

    return Point(x, y)


def quadraticBezier(p0, p1, p2, res=0.1):
    """
    Compute quadratic Bezier curve.

    Args:
        p0 (shapely.Point): first anchor point
        p1 (shapely.Point): control point
        p2 (shapely.Point): second anchor point
        res (float, optional): resolution of the curve, between 0.0 and 1.0
    
    Returns:
        curve_points (list[shapely.Point]): list of points representing the curve
    """
    curve_points = []
    for t in np.linspace(0, 1, int(1/res)):
        curve_points.append(_quad_lerp(p0, p1, p2, t))

    return curve_points


def cubicBezier(p0, p1, p2, p3, res=0.1):
    """
    Compute cubic Bezier curve.

    Args:
        p0 (shapely.Point): first anchor point
        p1 (shapely.Point): first control point
        p2 (shapely.Point): second control point
        p3 (shapely.Point): second anchor point
        res (float, optional): resolution of the curve, between 0.0 and 1.0
    
    Returns:
        curve_points (list[shapely.Point]): list of points representing the curve
    """
    curve_points = []
    for t in np.linspace(0, 1, int(1/res)):
        v1 = _quad_lerp(p0, p1, p2, t)
        v2 = _quad_lerp(p1, p2, p3, t)
        x = lerp(v1.x, v2.x, t)
        y = lerp(v1.y, v2.y, t)
        
        curve_points.append(Point(x, y))
    
    return curve_points


def catrom_point(p0, p1, p2, p3, t, tension=0.0):
    """Calculate point along spline curve using interpolation."""
    t2 = t * t
    t3 = t * t * t
    f0 = (tension - 1) / 2 * t3 + (1 - tension) * t2 + (tension - 1) / 2 * t
    f1 = (tension + 3) / 2 * t3 + (-5 - tension) / 2 * t2 + 1.0
    f2 = (-3 - tension) / 2 * t3 + (tension + 2) * t2 + (1 - tension) / 2 * t
    f3 = (1 - tension) / 2 * t3 + (tension - 1) / 2 * t2
    
    x = (p0.x * f0) + (p1.x * f1) + (p2.x * f2) + (p3.x * f3)
    y = (p0.y * f0) + (p1.y * f1) + (p2.y * f2) + (p3.y * f3)
    return Point(x, y)


def catrom_curve(control_points, res=0.5):
    """
    Construct curve from a sequence of points using Catmull-Rom spline segments.

    Args:
        control_points (list[shapely.Point]): list of four or more control points
        res (float, optional): resolution of a segment, between 0.0 and 1.0
    
    Returns:
        curve_points (list[shapely.Point]): list of points representing the curve
    """
    curve_points = []
    for i in range(0, len(control_points)-3):
        p0 = control_points[i]
        p1 = control_points[i+1]
        p2 = control_points[i+2]
        p3 = control_points[i+3]

        for t in np.linspace(0, 1, int(1/res)):
            curve_points.append(catrom_point(p0, p1, p2, p3, t))
    
    return curve_points