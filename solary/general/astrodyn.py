"""
astrodyn.py

Miscellaneous functions regarding astro-dynamical topics can be found here.

"""

# Import standard modules
import math

# Import solary
import solary

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

    Examples
    --------
    An example to compute the Tisserand parameter of the comet 67P/Churyumov–Gerasimenko. The data
    have been obtained from https://ssd.jpl.nasa.gov/sbdb.cgi?sstr=67P

    >>> import math
    >>> import solary
    >>> tisserand_tsch_geras_67p = solary.general.astrodyn.tisserand(sem_maj_axis_obj=3.46, \
                                                                     inc=math.radians(7.03), \
                                                                     ecc=0.64)
    >>> tisserand_tsch_geras_67p
    2.747580043374075

    """

    # If no semi-major axis of a larger object is given: Assume the planet Jupiter. Jupiter's
    # semi-major axis can be found in the config file
    if not sem_maj_axis_planet:

        # Get the constants config file
        config = solary.auxiliary.config.get_constants()
        sem_maj_axis_planet = float(config['planets']['sem_maj_axis_jup'])

    # Compute the tisserand parameter
    tisserand_parameter = (sem_maj_axis_planet / sem_maj_axis_obj) + 2.0 * math.cos(inc) \
                          * math.sqrt((sem_maj_axis_obj / sem_maj_axis_planet) * (1.0 - ecc**2.0))

    return tisserand_parameter


def kep_apoapsis(sem_maj_axis, ecc):
    """
    Compute the apoapsis, depending on the semi-major axis and eccentricity.

    Parameters
    ----------
    sem_maj_axis : float
        Semi-major axis of the object in any unit.
    ecc : float
        Eccentricity of the object.

    Returns
    -------
    apoapsis : float
        Apoapsis of the object. Unit is identical to input unit of sem_maj_axis.

    """

    apoapsis = (1.0 + ecc) * sem_maj_axis

    return apoapsis


def kep_periapsis(sem_maj_axis, ecc):
    """
    Compute the periapsis, depending on the semi-major axis and eccentricity.

    Parameters
    ----------
    sem_maj_axis : float
                Semi-major axis of the object in any unit.
    ecc : float
        Eccentricity of the object.

    Returns
    -------
    periapsis : float
        Periapsis of the object. Unit is identical to input unit of sem_maj_axis.

    """

    periapsis = (1.0 - ecc) * sem_maj_axis

    return periapsis


def mjd2jd(m_juldate):
    """
    Convert the given Julian Date to the Modified Julian Date.

    Parameters
    ----------
    m_juldate : float
        Modified Julian Date.

    Returns
    -------
    juldate : float
        Julian Date.

    """

    juldate = m_juldate + 2400000.5

    return juldate


def jd2mjd(juldate):
    """
    Convert the Modified Julian Date to the Julian Date.

    Parameters
    ----------
    juldate : float
        Julian Date.

    Returns
    -------
    m_juldate : float
        Modified Julian Date.

    """

    m_juldate = juldate - 2400000.5

    return m_juldate

def sphere_of_influence(sem_maj_axis, minor_mass, major_mass):
    """
    Compute the Sphere of Influence (SOI) of a minor object w.r.t. a major object, assuming a
    spherical SOI

    Parameters
    ----------
    sem_maj_axis : float
        Semi-Major Axis given in any physical dimension.
    minor_mass : float
        Mass of the minor object given in any physical dimension.
    major_mass : float
        Mass of the major object given in the same physical dimension as minor_mass.

    Returns
    -------
    soi_radius : float
        SOI radius given in the same physical dimension as sem_maj_axis.

    """

    # Compute the Sphere of Influence (SOI)
    soi_radius = sem_maj_axis * ((minor_mass / major_mass) ** (2.0 / 5.0))

    return soi_radius
