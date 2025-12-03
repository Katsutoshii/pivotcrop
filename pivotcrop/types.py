"""Common types."""

from typing import List, Tuple
import dataclasses


class PivotGroup:
    """Describes a group that has its own pivot."""


@dataclasses.dataclass
class IndependentDir:
    """
    A directory where each image needs to be cropped separately.
    """

    path: str
    round_to_num_pixels: int = 4


@dataclasses.dataclass
class BBoxGroup(List[str]):
    """
    Group of directories sharing the same bounding box.
    """

    paths: str | List[str]
    round_to_num_pixels: int = 4

    def __post_init__(self):
        if not isinstance(self.paths, list):
            self.paths = [paths]


class Pivot(Tuple[float, float]):
    """
    XY point defining a pivot point.
    """


Int2 = Tuple[int, int]
Int4 = Tuple[int, int, int, int]

PivotGroup = BBoxGroup | IndependentDir

X: int = 0
Y: int = 1
