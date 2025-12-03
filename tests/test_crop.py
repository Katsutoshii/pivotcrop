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
        output_dir="output/test_crop_images",
        root_dir="testdata",
        pivot_groups={(0.5, 1): [BBoxGroup(["Motion/A"]), IndependentDir("Motion/B")]},
    ).crop()
    assert Path("output/test_crop_images/Motion/A/Walk/Walk2a.png").exists()
    assert Path("output/test_crop_images/Motion/A/Walk/Walk3.png").exists()
    assert Path("output/test_crop_images/Motion/A/Walk/Walk3a.png").exists()
    assert Path("output/test_crop_images/Motion/B/Walk/Walk2a.png").exists()
    assert Path("output/test_crop_images/Motion/B/Walk/Walk3.png").exists()
    assert Path("output/test_crop_images/Motion/B/Walk/Walk3a.png").exists()
    assert Path("output/test_crop_images/Motion/B/Walk/Walk10a.png").exists()


def test_crop_images_no_rounding():
    """
    Test crop images
    """

    PivotCropper(
        output_dir="output/test_crop_images_no_rounding",
        root_dir="testdata",
        pivot_groups={
            (0.5, 1): [
                BBoxGroup(["Motion/A"], round_to_num_pixels=1),
                IndependentDir("Motion/B", round_to_num_pixels=1),
            ]
        },
    ).crop()
    assert Path("output/test_crop_images_no_rounding/Motion/A/Walk/Walk2a.png").exists()
    assert Path("output/test_crop_images_no_rounding/Motion/A/Walk/Walk3.png").exists()
    assert Path("output/test_crop_images_no_rounding/Motion/A/Walk/Walk3a.png").exists()
    assert Path("output/test_crop_images_no_rounding/Motion/B/Walk/Walk2a.png").exists()
    assert Path("output/test_crop_images_no_rounding/Motion/B/Walk/Walk3.png").exists()
    assert Path("output/test_crop_images_no_rounding/Motion/B/Walk/Walk3a.png").exists()
    assert Path(
        "output/test_crop_images_no_rounding/Motion/B/Walk/Walk10a.png"
    ).exists()
