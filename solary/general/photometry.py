"""
TBD
"""

# Import standard modules
import configparser
import math

def appmag2irr(app_mag):
    """
    Convert the apparent magnitude to the corresponding irradiance given in
    W/m^2.

    Parameters
    ----------
    app_mag : int or float
        Apparent bolometric magnitude given in mag.

    Returns
    -------
    irradiance : float
        Irradiance given in W/m^2.

    """

    # Load the configuration file that contains the zero point bolometric
    # irradiance
    config = configparser.ConfigParser()
    config.read('_config/constants.ini')
    appmag_irr_i0 = float(config['photometry']['appmag_irr_i0'])

    # Convert apparent magnitude to irradiance
    irradiance = 10.0 ** (-0.4 * app_mag + math.log10(appmag_irr_i0))

    return irradiance

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

    References
    ----------
    [1] https://www.britastro.org/asteroids/dymock4.pdf

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
