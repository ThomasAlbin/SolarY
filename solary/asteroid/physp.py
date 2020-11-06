"""
physp.py

This script contains miscellaneous functions to describe and derive physical and instrinsic
parameters of asteroids.

"""

# Import standard modules
import math


def ast_size(albedo, abs_mag):
    """
    Compute the radius of an asteroid by using the asteroid's albedo and absolute magnitude.

    Parameters
    ----------
    albedo : float
        Albedo of the object ranging within the intervall (0, 1].
    abs_mag : float
        Absolute magnitude of the object.

    Returns
    -------
    radius : float
        Radius of the object given in kilometer.

    References
    ----------
    [1] Chesley, Steven R.; Chodas, Paul W.; Milani, Andrea; Valsecchi, Giovanni B.; Yeomans,
        Donald K. (October 2002). Quantifying the Risk Posed by Potential Earth Impacts. Icarus.
        159 (2): 425
    [2] https://cneos.jpl.nasa.gov/tools/ast_size_est.html
    [3] http://www.physics.sfasu.edu/astro/asteroids/sizemagnitude.html

    Examples
    --------
    >>> import solary
    >>> ast_radius = solary.asteroid.physp.ast_size(albedo=0.15, abs_mag=10)
    >>> ast_radius
    17.157

    """

    # Compute the diameter in km
    diameter = (1329.0 / math.sqrt(albedo)) * 10.0 ** (-0.2 * abs_mag)

    # Convert the diameter to radius
    radius = diameter / 2.0

    return radius
