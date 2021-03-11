"""
test_geometry.py

Testing suite for SolarY/general/geometry.py

"""

# Import standard libraries
import math

import SolarY


def test_circle_area():
    """
    Testing the area computation of a perfect circle.

    Returns
    -------
    None.

    """

    # Compute the area of a unit circle
    circle_area_res1 = SolarY.general.geometry.circle_area(radius=1.0)
    assert circle_area_res1 == math.pi

    # Second example
    circle_area_res1 = SolarY.general.geometry.circle_area(radius=2.0)
    assert circle_area_res1 == math.pi * 4.0


def test_fwhm2std():
    """
    Testing the FWHM to standard deviation computation

    Returns
    -------
    None.

    """

    # Compute the standard deviation corresponding FWHM and vice versa
    sigma1_exp = 5.0
    fwhm1 = 2.0 * sigma1_exp * math.sqrt(2.0 * math.log(2))

    sigma1_res = SolarY.general.geometry.fwhm2std(fwhm1)
    assert sigma1_res == sigma1_exp
