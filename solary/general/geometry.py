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


def fwhm2std(fwhm):
    """
    Convert the Full Width at Half Maximum to the corresponding Gaussian standard deviation.

    Parameters
    ----------
    fwhm : float
        Full Width at Half Maximum.

    Returns
    -------
    gauss_sigma : float
        Standard deviation assuming a Gaussian distribution.

    """

    # Compute the standard deviation
    gauss_sigma = fwhm / (2.0 * math.sqrt(2.0 * math.log(2)))

    return gauss_sigma
