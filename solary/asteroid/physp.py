"""
TBD

"""

# Import standard modules
import math

def ast_size(albedo, abs_mag):
    """
    TBD

    Parameters
    ----------
    albedo : TYPE
        DESCRIPTION.
    abs_mag : TYPE
        DESCRIPTION.

    Returns
    -------
    radius : TYPE
        DESCRIPTION.

    References
    ----------
    [1] Chesley, Steven R.; Chodas, Paul W.; Milani, Andrea; Valsecchi, Giovanni B.; Yeomans,
        Donald K. (October 2002). Quantifying the Risk Posed by Potential Earth Impacts. Icarus.
        159 (2): 425
    [2] https://cneos.jpl.nasa.gov/tools/ast_size_est.html
    [3] http://www.physics.sfasu.edu/astro/asteroids/sizemagnitude.html

    """

    # Compute the diameter in km
    diameter = (1329.0 / math.sqrt(albedo)) * 10.0 ** (-0.2 * abs_mag)

    # Conver the diameter to m
    diameter *= 1000.0

    # Convert the diameter to radius
    radius = diameter / 2.0

    return radius
