# PivotCrop

This Python script consumes a list of input directories of PNG files and crops them.
The user must specify a pivot for each group of directories. This pivot location is guaranteed to be
Preserved during the crop. For example, `(0.5, 0.5)` ensures that the pivot is centered on the image.
Use config.py to edit the input config.

Email: joshikatsu@gmail.com

## Instructions

Install the package using `pip install pivotcrop`.

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

The config entries are meant to be relative to the current working directory.
The directory structure is preserved in the output.

Pivot x y is [0, 1], with [0, 0] at the top left.

![](https://docs.unity3d.com/StaticFiles/ScriptRefImages/RectXMinYMin.svg)

## Algorithm

We simply loop over all directories and keep track of minimum and maximum points for the bounding box.
The main complexity of this script comes from ensuring that the cropped image still has the same relative pivot as the original.

Consider an animation where all images can be encompassed by a bounding box $B = (\text{min}_x, \text{min}_y), (\text{max}_x, \text{max}_y)$.
Our algorithm produces a new bounding box $B' = (\text{min}_x', \text{min}_y'), (\text{max}_x', \text{max}_y')$.
We must adjust $B$ such that the relative position of the pivot $(P_x, P_y)$ is preserved, where $P_x, P_y \in (0.0, 1.0)$.

One way to describe this constraint is to say that on each axis, the lower bound must change proportionally to the upper bound. The ratio of this proprotion is determined by the corresponding component of the pivot.

If we define the change to our upper and lower bounds on the $x$ axis as:

$\Delta \text{min}_x = \text{min}_x - \text{min}_x'$

$\Delta \text{max}_x = \text{max}_x' - \text{max}_x$

To retain the same pivot point when cropping, we must make sure that the following ratio holds:

$$\frac{\Delta \text{min}_x}{\Delta \text{max}_x} = \frac{P_x}{(1 - P_x)}$$

For simplicity, let
$Pr_x = \frac{P_x}{(1 - P_x)}$ be the pivot ratio for the $x$-axis.

If we need to reduce the minimum to maintain the ratio ($\frac{\Delta \text{min}_x}{\Delta \text{max}_x} \gt Pr_x$), we subtract an offset term to $\text{min}_x$:

$$\frac{\Delta \text{min}_x - \text{Offset}_x}{\Delta \text{max}_x} = Pr_x$$

$$\Delta \text{min}_x - \text{Offset}_x = Pr_x \times \Delta \text{max}_x$$

$$\text{Offset}_x = \Delta \text{min}_x - Pr_x \times \Delta \text{max}_x$$

If we need to increase the maximum to maintain the ratio $\frac{\Delta \text{min}_x}{\Delta \text{max}_x} \lt Pr_x$, we add an offset to $\text{max}_x$:

$$\frac{\Delta \text{min}_x}{\Delta \text{max}_x - \text{Offset}_x} = Pr_x$$

$$\Delta \text{min}_x = Pr_x \times (\Delta \text{max}_x - \text{Offset}_x)$$

$$\frac{\Delta \text{min}_x}{Pr_x} = \Delta \text{max}_x - \text{Offset}_x$$

$$\text{Offset}_x  = \Delta \text{max}_x - \frac{\Delta \text{min}_x}{Pr_x}$$


Same deal for the $y$ axis.
