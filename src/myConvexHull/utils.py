"""
Basic utility tools for the library.
Contains many useful functions for processing and computing.
"""

from math import isclose, sqrt
from myConvexHull.types import Vector, Line, Point

def vec_len(v: Vector) -> float:
    """Calculate the length of a vector.

    Args:
        v (Vector): Vector reference.
    
    Returns:
        float: Length of he vector.
    """
    return sqrt(v[0] ** 2 + v[1] ** 2)

def dist_to_line(l: Line, p: Point) -> float:
    """Calculate the distance between a point and a line.

    Original Formula
    Distance between a point and a line given the line equation.
    d = |am+bn+c|/sqrt(a*a+b*b) ... (1)
    where line equation ax + by + c = 0 ... (2)

    Line equation given two points:
    (y-y1)/(x-x1) = (y2-y1)/(x2-x1)
    (y-y1)(x2-x1) = (y2-y1)(x-x1)
    (y-y1)(x2-x1) - (x-x1)(y2-y1) = 0
    x2y-x1y-x2y1+x1y1 - (xy2-xy1-x1y2+x1y1) = 0
    x2y - x1y - x2y1 + x1y1 - xy2 + xy1 + x1y2 - x1y1 = 0
    (x2-x1)y - x2y1 + x1y1 - x(y2-y1) + x1y2 - x1y1 = 0
    (y1-y2)x + (x2-x1)y - x2y1 + x1y2 = 0 ... (3)

    We can infer from (2) and (3) that
    a = y1-y2
    b = x2-x1
    c = -x2*y1 + x1*y2

    Thus the final distance formula is:
    d = abs(a*m + b*n + c) / sqrt(a^2 + b^2)

    Args:
        l (Line): Line reference.
        p (Point): Point distance reference.
    
    Returns:
        float: Distance between a point and a line.
    """
    a = l[0][1] - l[1][1]
    b = l[1][0] - l[0][0]
    c = - l[1][0] * l[0][1] + l[0][0] * l[1][1]
    return abs(a * p[0] + b * p[1] + c) / vec_len((a, b))

def det(l: Line, p: Point) -> float:
    """Calculate the determinant between a point and a line.

    Args:
        l (Line): Line reference.
        p (Point): Point determinant reference.
    
    Returns:
        float: Determinant between a point and a line.
            = 0: point is on the line.
            > 0: point is on the left side of the line.
            < 0: point is on the right side of the line.
    """
    res = (
        p[0] * l[0][1]
        + l[1][0] * p[1]
        + l[0][0] * l[1][1]
        - l[1][0] * l[0][1]
        - l[0][0] * p[1]
        - p[0] * l[1][1]
    )

    if isclose(res, 0, abs_tol=1e-13):
        res = 0
    return res

