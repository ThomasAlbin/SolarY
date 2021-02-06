"""
camera.py

Script that contains miscellaneous functions and classes for / of camera system (e.g., CCDs).

"""
import typing as t
# Import standard libraries
import json
from pathlib import Path
from dataclasses import dataclass


@dataclass
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

    """

    pixels: list  # type t.List[int, int]
    pixel_size: float
    dark_noise: float
    readout_noise: float
    full_well: t.Union[int, float]
    quantum_eff: float

    @staticmethod
    def load(config_path: t.Union[Path, str]) -> "CCD":
        """Factory method to construct a CCD object from a JSON file."""
        with Path(config_path).open(mode="r") as temp_obj:
            ccd_config = json.load(temp_obj)
            return CCD(**ccd_config)

    @property
    def chip_size(self) -> t.Tuple[float, float]:
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

        return chip_size[0], chip_size[1]


    @property
    def pixel_size_sq_m(self) -> float:
        """
        Get the size of a single pixel in m^2.

        Returns
        -------
        float
            Size of a single pixel. Given in m^2.

        """

        # Conversion between micro meter^2 to meter^2 -> 10^-12
        return (self.pixel_size ** 2.0) * (10.0 ** (-12))
