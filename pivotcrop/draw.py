"""Utils for drawing on PIL Images.
"""
from PIL import Image
from pivotcrop.types import Int2, Int4, X, Y


# pylint: disable=invalid-name
def draw_square(image: Image.Image, center: Int2, radius: int, color: Int4 = (255, 64, 64, 255)):
    """Draw a square at the given point. Used for debugging."""
    for i in range(radius * 2):
        for j in range(radius * 2):
            x: int = center[X] + i - radius
            y: int = center[Y] + j - radius
            if 0 <= y < image.width and 0 <= y < image.height:
                image.putpixel((x, y), color)
