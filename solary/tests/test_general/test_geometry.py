"""
test_geometry.py

Testing suite for solary/general/geometry.py

"""

# Import standard libraries
import math

# Import solary
import solary


def test_circle_area():
    """
    Testing the area computation of a perfect circle.

    Returns
    -------
    None.

    """

    # Compute the area of a unit circle
    circle_area_res1 = solary.general.geometry.circle_area(radius=1.0)
    assert circle_area_res1 == math.pi

    # Second example
    circle_area_res1 = solary.general.geometry.circle_area(radius=2.0)
    assert circle_area_res1 == math.pi * 4.0
