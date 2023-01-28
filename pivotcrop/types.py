"""Common types.
"""
# pylint: skip-file
from typing import List, Tuple


class PivotGroup:
    """Describes a group that has its own pivot.
    """


class IndependentDir(str):
    """
    A directory where each image needs to be cropped separately.
    """


class BBoxGroup(List[str]):
    """
    Group of directories sharing the same bounding box.
    """

    def __init__(self, *args):
        super().__init__(list(args))


class Pivot(Tuple[float, float]):
    """
    XY point defining a pivot point.
    """


Int2 = Tuple[int, int]
Int4 = Tuple[int, int, int, int]


X: int = 0
Y: int = 1
