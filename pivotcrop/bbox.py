"""Bounding box utils.
"""
import glob
import math
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import numpy as np
from PIL import Image

from pivotcrop.types import Pivot, X, Y


# pylint: disable=invalid-name
def round_down(v: int, n: int) -> int:
    """Round v down to the nearest multiple of n.
    `round(63, 4) -> 60`
    """
    return n * math.floor(v / n)


# pylint: disable=invalid-name
def round_up(v: int, n: int) -> int:
    """Round v up to the nearest multiple of n.
    `round(63, 4) -> 64`
    """
    return n * math.ceil(v / n)


@dataclass
class BoundingBox:
    """Defines a minimal bounding box (trimming as much whitespace as possible) in an image."""
    min_x: int
    min_y: int
    max_x: int
    max_y: int

    @staticmethod
    def from_image(image: Image) -> Optional["BoundingBox"]:
        """Constructs a bounding box from an image."""
        # `getbboxox` only trims the black border. Thus we must
        # first replace white border before computing the
        # bounding box.
        data = np.array(image)
        red, green, blue, alpha = data.T
        white_areas = (red == 255) & (blue == 255) & (
            green == 255) & (alpha == 0)
        # replace (255,255,255,0) with (0,0,0,0)
        data[..., :-1][white_areas.T] = (0, 0, 0)
        image = Image.fromarray(data)

        img_result = image.getbbox()
        if img_result is None:
            return None
        min_x, min_y, max_x, max_y = img_result
        return BoundingBox(min_x, min_y, max_x, max_y)

    def grow_to_fit(self, other: "BoundingBox"):
        """Grow this bounding box to fit another."""
        self.min_x = min(other.min_x, self.min_x)
        self.min_y = min(other.min_y, self.min_y)
        self.max_x = max(other.max_x, self.max_x)
        self.max_y = max(other.max_y, self.max_y)

    def round_bounds(self, n: int):
        """Rounds bounds the nearest nth pixel"""
        self.min_x = round_down(self.min_x, n)
        self.min_y = round_down(self.min_y, n)
        self.max_x = round_up(self.max_x, n)
        self.max_y = round_up(self.max_y, n)

    def __str__(self) -> str:
        return f"({self.min_x}, {self.min_y}) ({self.max_x}, {self.max_y})"

    def crop(self, image: Image) -> Image:
        """Crops an image using this bounding box."""
        return image.crop((self.min_x, self.min_y, self.max_x, self.max_y))

    @staticmethod
    def load_dirs(root_path: Path, input_dirs: List[str]) -> List[Optional["BoundingBox"]]:
        """Loads image boundting boxes from the directory."""
        bboxes: List[Optional[BoundingBox]] = []

        for input_dir in input_dirs:
            input_path: Path = root_path / input_dir
            for infile in glob.glob(f"{input_path}/**/*.png", recursive=True):
                with Image.open(infile) as image:
                    bboxes.append(BoundingBox.from_image(image))

        return bboxes

    @staticmethod
    def compose(bboxes: List[Optional["BoundingBox"]]) -> Optional["BoundingBox"]:
        """Get the bounding box that covers all images in a directory and
        overwrites with a cropped version.
        """
        total_bbox: Optional[BoundingBox] = None
        for bbox in bboxes:
            if bbox is not None:
                if total_bbox is None:
                    total_bbox = copy(bbox)
                else:
                    total_bbox.grow_to_fit(bbox)

        total_bbox.round_bounds(4)
        return total_bbox

    def resize_with_pivot(self,  pivot: Pivot,
                          total_bbox: Optional["BoundingBox"] = None) -> "BoundingBox":
        """Given a bounding box that is contained within `total_bbox`,
        Return `bbox` shrunk as much as possible while keeping `pivot` at
        the same relative location.
        """
        if total_bbox is None:
            total_bbox = self
        adjusted_bbox: BoundingBox = copy(self)

        if pivot[X] == 0.0:
            adjusted_bbox.min_x = total_bbox.min_x
        elif pivot[X] == 1.0:
            adjusted_bbox.max_x = total_bbox.max_x
        else:
            pivot_ratio_x: float = pivot[X] / (1 - pivot[X])
            d_min_x: int = self.min_x - total_bbox.min_x
            d_max_x: int = total_bbox.max_x - self.max_x

            # If the min shrunk too much relative to the max
            if d_max_x == 0 or (d_min_x / d_max_x) > pivot_ratio_x:
                offset_x = int(d_min_x - d_max_x * pivot_ratio_x)
                adjusted_bbox.min_x -= offset_x
            else:
                offset_x = int(d_max_x - d_min_x / pivot_ratio_x)
                adjusted_bbox.max_x += offset_x

        if pivot[Y] == 0.0:
            adjusted_bbox.min_y = total_bbox.min_y
        elif pivot[Y] == 1.0:
            adjusted_bbox.max_y = total_bbox.max_y
        else:
            pivot_ratio_y: float = pivot[Y] / (1 - pivot[Y])
            d_min_y: int = self.min_y - total_bbox.min_y
            d_max_y: int = total_bbox.max_y - self.max_y

            # If the min shrunk too much relative to the max
            if d_max_y == 0 or (d_min_y / d_max_y) > pivot_ratio_y:
                offset_y = int(d_min_y - d_max_y * pivot_ratio_y)
                adjusted_bbox.min_y -= offset_y
            else:
                offset_y = int(d_max_y - d_min_y / pivot_ratio_y)
                adjusted_bbox.max_y += offset_y

        adjusted_bbox.round_bounds(4)

        return adjusted_bbox
