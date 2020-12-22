"""
geometry.py

Auxiliary functions for geometric purposes.

"""

# Import standard libraries
import math


def circle_area(radius):
    """
    Compute the area of a perfect with a given radius.

    Parameters
    ----------
    radius : float
        Radius of the circle given in any dimension.

    Returns
    -------
    area : float
        Area of the circle, given in the input dimension^2.

    """

    # Compute the area of a circle
    area = math.pi * (radius ** 2.0)

    return area
