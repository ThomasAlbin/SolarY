"""
test_physp.py

Testing suite for SolarY/asteroid/physp

"""
import pytest

import SolarY.asteroid


def test_ast_size():
    """
    Test function for the asteroid size computation function

    Returns
    -------
    None.

    """

    # Compute the radius of an asteroid (test 1) and compare it with the (approximated expectation)
    ast_radius1 = SolarY.asteroid.physp.ast_size(albedo=0.05, abs_mag=10.0)
    assert pytest.approx(ast_radius1) == 29.71734

    # Compute the radius of an asteroid (test 2) and compare it with the (approximated expectation)
    ast_radius2 = SolarY.asteroid.physp.ast_size(albedo=0.3, abs_mag=20.0)
    assert pytest.approx(ast_radius2) == 0.12132055

    # Compute the radius of an asteroid (test 3) and compare it with the (approximated expectation)
    ast_radius3 = SolarY.asteroid.physp.ast_size(albedo=0.15, abs_mag=26.0)
    assert pytest.approx(ast_radius3) == 0.010825535
