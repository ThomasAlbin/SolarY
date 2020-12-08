"""
config.py

Auxiliary functions for all library relevant configuration files

"""

# Import standard libraries
import configparser
import os

# Import the ROOT directory of SolarY
from solary import ROOT_DIR


def get_constants():
    """
    Function to get the constants.ini file from the _config directory

    Returns
    -------
    config : configparser.ConfigParser
        Configuration Parser that constains miscellaneous constants (like astrodynmical, time,
        etc.)

    """

    # Set config parser
    config = configparser.ConfigParser()

    # Get the constants ini file
    constants_ini_path = os.path.join(ROOT_DIR, '_config', 'constants.ini')

    # Read and parse the config file
    config.read(constants_ini_path)

    return config
