"""
camera.py

Script that contains miscellaneous functions and classes for / of camera system (e.g., CCDs).

"""

# Import standard libraries
import json


def read_ccd_config(config_filepath):
    """
    Function to read the configuration file for a CCD system.

    Parameters
    ----------
    config_filepath : str
        File path of the configuration file.

    Returns
    -------
    ccd_config : dict
        CCD configuration.

    """

    # Open the file path and load / read it as a JSON
    with open(config_filepath) as temp_obj:
        ccd_config = json.load(temp_obj)

    return ccd_config


class CCD:
    """
    Class that defines ande describes a CCD camera. Properties are derived from the user's input
    like e.g., the chip size.

    Attributes
    ----------
    pixels : list
        List with the number of pixels per dimension.
    pixel_size : float
        Size of a single pixel, assuming a square shaped pixel. Given in micro meter.
    dark_noise : float
        Dark noise / current of a single pixel. Given in electrons^-1 * s^-1 * pixel^-1.
    readout_noise : float
        Readout noise of a single pixel. Given in electrons^-1 * pixel^-1.
    full_well : int or float
        Number of max. electrons per pixel.

    Static Properties
    -----------------
    chip_size : list
        List with the size of the CCD chip in each dimension (x, y). Given in mm.
    pixel_size_sq_m : float
        Size of a single pixel, assuming a square shaped pixel. Given in m^2.

    """


    def __init__(self, ccd_config):
        """
        Init function.

        Parameters
        ----------
        ccd_config : dict
            CCD configuration dictionary.

        Returns
        -------
        None.

        """

        # Placeholders for the static attributes
        self.pixels = [None, None]
        self.pixel_size = None
        self.dark_noise = None
        self.readout_noise = None
        self.full_well = None
        self.quantum_eff = None

        # Set the attributes dynamically in a for loop and set the values accordingly.
        valid_keys = ['pixels', 'pixel_size', 'dark_noise', 'readout_noise', 'full_well',
                      'quantum_eff']
        for key in valid_keys:
            setattr(self, key, ccd_config.get(key))


    @property
    def chip_size(self):
        """
        Get the chip size (x and y dimension). Given in mm.

        Returns
        -------
        chip_size : list
                    List with the size of the CCD chip in each dimension (x, y). Given in mm.

        """

        # Placeholder list for the results
        chip_size = []

        # Convert the pixel size, given in micro meter, to mm.
        pixel_size_mm = self.pixel_size / 1000.0

        # Compute the chip size in each dimension by multiplying the number of pixels with the
        # pixel size, given in mm.
        for pixel_dim in self.pixels:
            chip_size.append(pixel_dim*pixel_size_mm)

        return chip_size


    @property
    def pixel_size_sq_m(self):
        """
        Get the size of a single pixel in m^2.

        Returns
        -------
        float
            Size of a single pixel. Given in m^2.

        """

        # Conversion between micro meter^2 to meter^2 -> 10^-12
        return (self.pixel_size ** 2.0) * (10.0 ** (-12))
