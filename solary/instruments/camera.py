"""Miscellaneous functions and classes for / of camera system (e.g., CCDs).

.. |dot|   unicode:: U+2219  .. BULLET OPERATOR
"""
import json
import typing as t
from pathlib import Path


class CCD:
    """Class that defines ande describes a CCD camera.

    Properties are derived from the user's input like e.g., the chip size.
    """

    def __init__(
        self,
        pixels: t.Tuple[int, int],
        pixel_size: float,
        dark_noise: float,
        readout_noise: float,
        full_well: t.Union[int, float],
        quantum_eff: float,
    ) -> None:
        r"""CCD camera initializer.

        Parameters
        ----------
        pixels: (int, int)
            List with the number of pixels per dimension.
        pixel_size: float
            Size of a single pixel, assuming a square shaped pixel. Given in micro meter.
        dark_noise: float
            Dark noise / current of a single pixel.
            Given in: `electrons`\ :sup:`-1` |dot| `s`\ :sup:`-1` |dot| `pixel`\ :sup:`-1`
        readout_noise: float
            Readout noise of a single pixel. Given in electrons^-1 * pixel^-1.
        full_well: t.Union[int, float]
            Number of max. electrons per pixel.
        quantum_eff: float
            Quantum efficiency of the sensor. Allowed values: 0.0 qe < 1.0
        """
        self._pixels = pixels
        self._pixel_size = pixel_size
        self._dark_noise = dark_noise
        self._readout_noise = readout_noise
        self._full_well = full_well
        self._quantum_eff = quantum_eff

    @staticmethod
    def load_from_json_file(config_path: t.Union[Path, str]) -> "CCD":
        """Construct a CCD object from a JSON file."""
        with Path(config_path).open(mode="r") as temp_obj:
            ccd_config = json.load(temp_obj)
            return CCD(**ccd_config)

    @property
    def pixels(self) -> t.Tuple[int, int]:
        """List with the number of pixels per dimension (w x h)."""
        return self._pixels

    @property
    def pixel_size(self) -> float:
        """Size of a single pixel, assuming a square shaped pixel in um."""
        return self._pixel_size

    @property
    def dark_noise(self) -> float:
        """Dark noise / current of a single pixel."""
        return self._dark_noise

    @property
    def readout_noise(self) -> float:
        """Readout noise of a single pixel in electrons^-1 * pixel^-1."""
        return self._readout_noise

    @property
    def full_well(self) -> float:
        """Return the maximum number of electrons per pixel."""
        return self._full_well

    @property
    def quantum_eff(self) -> float:
        """Quantum efficiency of the sensor 0 < QE < 1.0."""
        return self._quantum_eff

    @property
    def chip_size(self) -> t.Tuple[float, float]:
        """[float, float]: Get the chip size (x and y dimension). Given in mm."""
        # Placeholder list for the results
        chip_size = []

        # Convert the pixel size, given in micro meter, to mm.
        pixel_size_mm = self.pixel_size / 1000.0

        # Compute the chip size in each dimension by multiplying the number of
        # pixels with the pixel size, given in mm.
        for pixel_dim in self.pixels:
            chip_size.append(pixel_dim * pixel_size_mm)

        return chip_size[0], chip_size[1]

    @property
    def pixel_size_sq_m(self) -> float:
        """float: Get the size of a single pixel in m^2."""
        # Conversion between micro meter^2 to meter^2 -> 10^-12
        return (self.pixel_size ** 2.0) * (10.0 ** (-12))
