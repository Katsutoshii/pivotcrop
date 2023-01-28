"""Defines the main cropper class for pivot based cropping.
"""
import glob
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union, Dict

from PIL import Image

from pivotcrop import log
from pivotcrop.bbox import BoundingBox
from pivotcrop.draw import draw_square
from pivotcrop.types import BBoxGroup, IndependentDir, Pivot, X, Y


# pylint: disable=too-many-instance-attributes
@dataclass
class PivotCropper:
    """PivotCropper class that enables cropping iamges in directories based on a pivot point.

    Example usage:
    ```py
    from pivotcrop import PivotCropper

    PivotCropper(
        output_dir="output",
        root_dir="testdata",
        pivot_groups={
            # All directories with images using pivot (0.5, 1) should be configured here.
            (0.5, 1): [
                # Two directories that should share the same bounding box.
                BBoxGroup("Images/A", "Images/B"),
                # Another directory using same pivot, but a different bounding box.
                BBoxGroup("Images/C")
            ],
            # Entry with a different pivot
            (0.5, 0.5): [
                BBoxGroup("Images/D"),
                # A directory where each image gets its own bounding box.
                IndependentDir("Images/E")
            ],
        }
    ).crop()
    ```
    """

    # Relative or absolute path to output cropped images.
    output_dir: Union[str, Path]

    # Root directory combined with given input directories
    root_dir: Union[str, Path]

    # Mapping of pivot to pivot group.
    pivot_groups: Dict[Pivot, List[Union[BBoxGroup, IndependentDir]]
                       ] = field(default_factory=dict)

    verbosity: log.Verbosity = log.Verbosity.INFO
    logger: log.Logger = log.Logger(verbosity)

    # If true, plot the pivot point on the image.
    debug: bool = False
    debug_memory: bool = False

    def __post_init__(self):
        self.root_path = Path(self.root_dir)
        self.output_path = Path(self.output_dir)

    def crop(self):
        """Crops all images provided in the config."""
        for pivot, groups in self.pivot_groups.items():
            self.logger.info(f"Cropping images for pivot {pivot}")
            for group in groups:
                if isinstance(group, BBoxGroup):
                    self.crop_group(group, pivot)
                elif isinstance(group, IndependentDir):
                    self.crop_dir(self.root_path / group, pivot)
                else:
                    self.logger.error(f"Malformed config: {group}")

    def crop_image(self, image: Image.Image, pivot: Pivot,
                   total_bbox: Optional[BoundingBox] = None) -> Optional[Image.Image]:
        """Crops a single image according to the given pivot."""
        bbox = BoundingBox.from_image(image)
        if bbox is None:
            self.logger.warning("WARNING: found empty image.")
            return None

        adjusted_bbox: BoundingBox = bbox.resize_with_pivot(pivot, total_bbox)
        return adjusted_bbox.crop(image)

    def save_image(self, image: Image.Image, path: Path):
        """Saves an image at the given path, creating the parent dir if necessary."""
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
        self.logger.info(f"     Saved to {path}")

    def crop_dir(self, path: Path, pivot: Pivot, total_bbox: Optional[BoundingBox] = None):
        """Crops an entire directory of images.

        If total_bbox is specified, then the directories share a max bounding box.
        """
        self.logger.info(f"  Cropping images in directory {path}")
        for infile in glob.glob(f"{path}/**/*.png", recursive=True):
            self.logger.info(f"    Cropping image {infile}")
            with Image.open(infile) as image:
                cropped_image = self.crop_image(image, pivot, total_bbox)
                if cropped_image is None:
                    continue

                if self.debug:
                    self.debug_pivot(pivot, cropped_image)

                outfile = (self.output_path /
                           Path(infile).relative_to(self.root_path))
                self.save_image(cropped_image, outfile)

                if self.debug_memory:
                    initial_kb = os.path.getsize(infile) >> 10
                    cropped_kb = os.path.getsize(outfile) >> 10
                    self.logger.info(
                        f"  Decreased image size from {initial_kb}KB to {cropped_kb}KB")

    def crop_group(self, bbox_group: BBoxGroup, pivot: Pivot):
        """Crops a gorup of directories all sharing the same total bounding box."""

        bbs: List[Optional[BoundingBox]] = BoundingBox.load_dirs(
            self.root_path, bbox_group)
        if len(bbs) == 0:
            self.logger.error("    Input directories had no .png files.")
            return

        total_bb: Optional[BoundingBox] = BoundingBox.compose(bbs)

        for input_dir in bbox_group:
            self.crop_dir(self.root_path / input_dir, pivot, total_bb)

    def debug_pivot(self, pivot: Pivot, image: Image.Image):
        """Debugs pivot selection by plotting it on the image."""
        pivot_x = int(image.width *
                      pivot[X])
        pivot_y = int(image.height * pivot[Y])
        draw_square(image,
                    (pivot_x, pivot_y), radius=4)
