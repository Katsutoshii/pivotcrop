"""
Basic unit tests for autocrop.
"""
from pathlib import Path

from pivotcrop import PivotCropper, IndependentDir, BBoxGroup


def test_crop_images():
    """
    Test crop images
    """

    PivotCropper(
        output_dir="output",
        root_dir="testdata",
        pivot_groups={
            (0.5, 1): [
                BBoxGroup("Motion/A"),
                IndependentDir("Motion/B")
            ]
        }
    ).crop()
    assert Path("output/Motion/A/Walk/Walk2a.png").exists()
    assert Path("output/Motion/A/Walk/Walk3.png").exists()
    assert Path("output/Motion/A/Walk/Walk3a.png").exists()
    assert Path("output/Motion/B/Walk/Walk2a.png").exists()
    assert Path("output/Motion/B/Walk/Walk3.png").exists()
    assert Path("output/Motion/B/Walk/Walk3a.png").exists()
    assert Path("output/Motion/B/Walk/Walk10a.png").exists()
