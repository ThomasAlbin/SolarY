"""
photometry.py

This module contains functions for photometric purposes.

"""

# Import standard modules
import math

# Import solary
import solary


def appmag2irr(app_mag):
    """
    Convert the apparent magnitude to the corresponding irradiance given in
    W/m^2. The zero point magnitude is provided by the IAU in [1].

    Parameters
    ----------
    app_mag : int or float
        Apparent bolometric magnitude given in mag.

    Returns
    -------
    irradiance : float
        Irradiance given in W/m^2.

    References
    ----------
    [1] https://www.iau.org/static/resolutions/IAU2015_English.pdf

    Examples
    --------
    >>> import solary
    >>> irradiance = solary.general.photometry.appmag2irr(app_mag=8.0)
    >>> irradiance
    1.5887638447672732e-11

    """

    # Load the configuration file that contains the zero point bolometric
    # irradiance
    config = solary.auxiliary.config.get_constants()
    appmag_irr_i0 = float(config['photometry']['appmag_irr_i0'])

    # Convert apparent magnitude to irradiance
    irradiance = 10.0 ** (-0.4 * app_mag + math.log10(appmag_irr_i0))

    return irradiance


def intmag2surmag(intmag, area):
    """
    Convert the integrated magnitude, given over a certain area in the sky to the corresponding
    surface brightness.

    Parameters
    ----------
    intmag : float
        Integrated magnitude given in mag.
    area : float
        Area of the object given in arcsec^2.

    Returns
    -------
    surface_mag : float
        Surface brightness of the object given in mag/arcsec^2.

    """

    # Compute the surface brightness
    surface_mag = intmag + 2.5 * math.log10(area)

    return surface_mag


def surmag2intmag(surmag, area):
    """
    Convert the surface brightness and a sky area to an integrated magnitude. The integrated
    magnitude can later be used to e.g., convert the night sky background brightness to an
    irradiance.

    Parameters
    ----------
    surmag : float
        Surface brightness given in mag/arcsec^2.
    area : float
        Area given in arcsec^2.

    Returns
    -------
    intmag : float
        Integrated magnitude given in mag.

    """

    # Compute the integrated magnitude
    intmag = surmag - 2.5 * math.log10(area)

    return intmag


def phase_func(index, phase_angle):
    """
    Phase function that is needed for the H-G visual / apparent magnitude function. The function
    has two versions, depending on the index ('1' or '2'). See [1].

    Parameters
    ----------
    index : str
        Phase function index / version. '1' or '2'.
    phase_angle : float
        Phase angle of the asteroid in radians (Angle as seen from the asteroid, pointing to
                                                a light source (Sun) and the observer (Earth)).

    Returns
    -------
    phi : float
        Phase function result.

    See Also
    --------
    hg_app_mag : Computing the visual / apparent magnitude of an object

    References
    ----------
    [1] https://www.britastro.org/asteroids/dymock4.pdf

    Examples
    --------
    >>> import math
    >>> import solary
    >>> phi1 = solary.general.photometry.phase_func(index=1, phase_angle=math.pi/4.0)
    >>> phi1
    0.14790968630394927
    >>> phi2 = solary.general.photometry.phase_func(index=2, phase_angle=math.pi/4.0)
    >>> phi2
    0.5283212147726485

    """

    # Dictionaries that contain the A and B constants, depending on the index version
    a_factor = {1: 3.33, \
                2: 1.87}
    b_factor = {1: 0.63, \
                2: 1.22}

    # Phase function
    phi = math.exp(-1.0 * a_factor[index] * ((math.tan(0.5 * phase_angle) ** b_factor[index])))

    # Return the phase function result
    return phi


def reduc_mag(abs_mag, phase_angle, slope_g=0.15):
    """
    Function to compute the reduced magnitude of an object. This function is needed for the
    H-G visual / apparent magnitude function. See [1]

    Parameters
    ----------
    abs_mag : float
        Absolute magnitude of the object.
    phase_angle : float
        Phase angle of the object w.r.t. the illumination source and observer.
    slope_g : float, optional
        Slope parameter G for the reduced magnitude. The set default value can be applied for
        asteroids with unknown slope parameter and the interval is (0, 1). The default is 0.15.

    Returns
    -------
    reduced_magnitude : float
        Reduced magnitude of the object.

    See Also
    --------
    hg_app_mag : Computing the visual / apparent magnitude of an object

    References
    ----------
    [1] https://www.britastro.org/asteroids/dymock4.pdf

    Examples
    --------
    >>> import math
    >>> import solary
    >>> reduced_magnitude = solary.general.photometry.reduc_mag(abs_mag=10.0, \
                                                                phase_angle=math.pi/4.0, \
                                                                slope_g=0.10)
    >>> reduced_magnitude
    11.826504643588578

    Per default, the slope parameter G is set to 0.15 and fits well for most asteroids

    >>> reduced_magnitude = solary.general.photometry.reduc_mag(abs_mag=10.0, \
                                                                phase_angle=math.pi/4.0)
    >>> reduced_magnitude
    11.720766748872016

    """

    # Compute the reduced magnitude based on the equations given in the references [1]
    reduced_magnitude = abs_mag - 2.5 * math.log10((1.0 - slope_g) \
                                                   * phase_func(index=1, phase_angle=phase_angle) \
                                                   + slope_g \
                                                   * phase_func(index=2, phase_angle=phase_angle))

    return reduced_magnitude


def hg_app_mag(abs_mag, vec_obj2obs, vec_obj2ill, slope_g=0.15):
    """
    Compute the visual / apparent magnitude of an asteroid, based on the H-G system [1], where H
    represents the absolute magnitude and G represents the magnitude slope parameter.

    Parameters
    ----------
    abs_mag : float
        Absolute magnitude.
    vec_obj2obs : list
        3 dimensional vector the contains the directional information (x, y, z) from the asteroid
        to the observer given in AU.
    vec_obj2ill : list
        3 dimensional vector the contains the directional information (x, y, z) from the asteroid
        to the illumination source given in AU.
    slope_g : float, optional
        Slope parameter G for the reduced magnitude. The set default value can be applied for
        asteroids with unknown slope parameter and the interval is (0, 1). The default is 0.15.

    Returns
    -------
    app_mag : float
        Apparent / visual (bolometric) magnitude of the asteroid as seen from the observer.

    References
    ----------
    [1] https://www.britastro.org/asteroids/dymock4.pdf

    Examples
    --------
    >>> import solary
    >>> apparent_magnitude = solary.general.photometry.hg_app_mag(abs_mag=10.0, \
                                                                  vec_obj2obs=[-1.0, 0.0, 0.0], \
                                                                  vec_obj2ill=[-2.0, 0.0, 0.0], \
                                                                  slope_g=0.10)
    >>> apparent_magnitude
    11.505149978319906

    """

    # Compute the length of the two input vectors
    vec_obj2obs_norm = solary.general.vec.norm(vec_obj2obs)
    vec_obj2ill_norm = solary.general.vec.norm(vec_obj2ill)

    # Compute the phase angle of the asteroid
    obj_phase_angle = solary.general.vec.phase_angle(vec_obj2obs, vec_obj2ill)

    # Compute the reduced magnitude of the asteroid
    red_mag = reduc_mag(abs_mag, obj_phase_angle, slope_g)

    # Merge all information and compute the apparent magnitude of the asteroid as seen from the
    # observer
    app_mag = red_mag + 5.0 * math.log10(vec_obj2obs_norm * vec_obj2ill_norm)

    return app_mag
