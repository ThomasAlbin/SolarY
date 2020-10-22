"""
astrodyn.py

Miscellaneous functions regarding astro-dynamical topics can be found here.
"""

# Import standard modules
import configparser
import math
import os

def tisserand(sem_maj_axis_obj, inc, ecc, sem_maj_axis_planet=None):
    """
    Compute the Tisserand parameter of an object w.r.t. a larger object. If no semi-major axis of
    a larger object is given, the values for Jupiter are assumed.

    Parameters
    ----------
    sem_maj_axis_obj : float
        Semi-major axis of the minor object (whose Tisserand parameter shall be computed) given in
        AU.
    inc : float
        Inclination of the minor object given in radians.
    ecc : float
        Eccentricity of the minor object.
    sem_maj_axis_planet : float, optional
        Semi-major axis of the major object. If no value is given, the semi-major axis of Jupiter
        is taken. The default is None.

    Returns
    -------
    tisserand_parameter : float
        Tisserand parameter of the minor object w.r.t. the major object.

    Notes
    -----
    The Tisserand parameter provides a dimensionless value for the astro-dyamical relation between
    e.g., comets and Jupiter. Let's assume one wants to compute the Tisserand parameter of a comet
    with the largest gas giant. A Tisserand parameter between 2 and 3 (2 < Tisserand < 3) indicates
    a so called Jupiter-Family Comet (JFC).

    """
    # If no semi-major axis of a larger object is given: Assume the planet Jupiter. Jupiter's
    # semi-major axis can be found in the config file
    if not sem_maj_axis_planet:

        # Set config parser
        config = configparser.ConfigParser()

        # Find the constants.ini
        module_path = os.path.dirname(__file__)
        constants_ini_path = os.path.join(module_path, '..', '_config', 'constants.ini')

        # Read and parse the config file
        config.read(constants_ini_path)
        sem_maj_axis_planet = float(config['planets']['sem_maj_axis_jup'])

    # Compute the tisserand parameter
    tisserand_parameter = (sem_maj_axis_planet / sem_maj_axis_obj) + 2.0 * math.cos(inc) \
                          * math.sqrt((sem_maj_axis_obj / sem_maj_axis_planet) * (1.0 - ecc**2.0))

    return tisserand_parameter

def kep_apoapsis(sem_maj_axis, ecc):

    apsis = (1.0 + ecc) * sem_maj_axis

    return apsis

def kep_periapsis(sem_maj_axis, ecc):

    apsis = (1.0 - ecc) * sem_maj_axis

    return apsis

def mjd2jd(m_juldate):

    juldate = m_juldate + 2400000.5

    return juldate

def jd2mjd(juldate):

    m_juldate = juldate - 2400000.5

    return m_juldate
