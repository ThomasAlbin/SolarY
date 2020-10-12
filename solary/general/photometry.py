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
