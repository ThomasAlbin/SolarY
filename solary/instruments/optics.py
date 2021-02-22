"""Implements classes and functions that are needed for optical systems."""
# pylint: disable=no-member
import json
import typing as t
from pathlib import Path

import solary


class Reflector:
    """
    Class that defines the optical system of a reflector telescope.

    The class is a base class for a high level telescope class and dictionary
    configurations to set attributes. Properties are derived from the user's
    input like e.g. the collector area of a telescope.
    """

    def __init__(
        self,
        main_mirror_dia: float,
        sec_mirror_area: float,
        optical_throughput: float,
        focal_length: float,
    ) -> None:
        """Init function.

        Parameters
        ----------
        main_mirror_dia : float
            Diameter of the main mirror. Given in m.
        sec_mirror_area : float
            Diameter of the secondary mirror. Given in m.
        optical_throughput: float
            Throughput of the telescope. The Throughput is a combination of
            the mirror reflectivity, filter transmissivity etc. It describes
            only the optical system and does no include e.g., the quantum
            efficiency of a camera system.
            Dimensionless and defined between 0 and 1.
        focal_length : float
            Focal length of the system. Given in m.
        """
        self._main_mirror_dia = main_mirror_dia
        self._sec_mirror_dia = sec_mirror_area
        self._optical_throughput = optical_throughput
        self._focal_length = focal_length

    @staticmethod
    def load_from_json_file(config_path: t.Union[Path, str]) -> "Reflector":
        """Construct a Reflector object from a JSON file.

        Parameters
        ----------
        config_path: t.Union[Path, str]
            The JSON configuration file location.

        Returns
        -------
        Reflector
            A Reflector instance.
        """
        with Path(config_path).open(mode="r") as temp_obj:
            config = json.load(temp_obj)
            return Reflector(**config)

    @property
    def main_mirror_dia(self) -> float:
        """Diameter of the main mirror in meters."""
        return self._main_mirror_dia

    @property
    def sec_mirror_dia(self) -> float:
        """Diameter of the secondary mirror in meters."""
        return self._sec_mirror_dia

    @property
    def optical_throughput(self) -> float:
        """Throughput of the telescope.

        The Throughput is a combination of the mirror reflectivity,
        filter transmissivity etc. It describes only the optical system and does no include e.g.,
        the quantum efficiency of a camera system. Dimensionless and defined between 0 and 1.
        """
        return self._optical_throughput

    @property
    def focal_length(self) -> float:
        """Focal length of the system in meters."""
        return self._focal_length

    @property
    def main_mirror_area(self) -> float:
        """Get the main mirror area, assuming a circular shaped mirror.

        Returns
        -------
        float
            Main mirror area. Given in m^2.
        """
        # Call a sub-module that requires the radius as an input
        return solary.general.geometry.circle_area(self.main_mirror_dia / 2.0)

    @property
    def sec_mirror_area(self) -> float:
        """Get the secondary mirror area in m^2, assuming a circular shaped mirror."""
        # Call a sub-module that requires the radius as an input
        return solary.general.geometry.circle_area(self.sec_mirror_dia / 2.0)

    @property
    def collect_area(self) -> float:
        """Get the photon collection area in m^2.

        This property simply substracts the secondary mirror area from the main one.
        """
        return self.main_mirror_area - self.sec_mirror_area
