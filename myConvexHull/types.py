"""
Custom type definitions.
"""
from typing import Tuple, Union

Vector = Point = Tuple[float, float]
PointIndex = int
Line = Tuple[Point, Point]
LineIndex = Tuple[PointIndex, PointIndex]
Feature = Union[int, str]
