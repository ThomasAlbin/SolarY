# pylint: disable=no-member
"""
optics.py

This script contains classes and functions that are needed for optical systems.

"""

# Import standard libraries
import typing as t
import json

# Import solary
import solary


def read_reflector_config(config_filepath: str) -> t.Dict[str, t.Any]:
    """
    Function to read the configuration file for a reflector system.

    Parameters
    ----------
    config_filepath : str
        File path of the configuration file.

    Returns
    -------
    optics_config : dict
        Reflector configuration.

    """

    # Open the file path and load / read it as a JSON
    with open(config_filepath) as temp_obj:
        optics_config = json.load(temp_obj)

    return optics_config


class Reflector:
    """
    Class that defines the optical system of a reflector telescope. The class is a base class for
    a high level telescope class and dictionary configurations to set attributes. Properties are
    derived from the user's input like e.g. the collector area of a telescope.

    Attributes
    ----------
    main_mirror_dia : float
        Diameter of the main mirror. Given in m.
    sec_mirr_dia : float
        Diameter of the secondary mirror. Given in m.
    optical_throughput: float
        Throughput of the telescope. The Throughput is a combination of the mirror reflectivity,
        filter transmissivity etc. It describes only the optical system and does no include e.g.,
        the quantum efficiency of a camera system. Dimensionless and defined between 0 and 1.
    focal_length : float
        Focal length of the system. Given in m.
    """

    """
    (sphinx complains)
    Static Properties
    -----------------
    main_mirror_area : float
        Main mirror area, assuming a circular mirror. Given in m^2.
    sec_mirror_area : float
        Secondary mirror area, assuming a cirular mirror. Given in m^2.
    collect_area : float
        Effective photon collection area (main mirror area substracted by the secondary mirror area)

    """


    def __init__(self, optics_config: t.Dict[str, t.Any]) -> None:
        """
        Init function.

        Parameters
        ----------
        optics_config : dict
            Reflector configuration dictionary.

        Returns
        -------
        None.

        """

        # Setting attribute placeholders
        self.main_mirror_dia = optics_config["main_mirror_dia"]
        self.sec_mirror_dia = optics_config["sec_mirror_dia"]
        self.optical_throughput = optics_config["optical_throughput"]
        self.focal_length = optics_config["focal_length"]


    @property
    def main_mirror_area(self) -> float:
        """
        Get the main mirror area, assuming a circular shaped mirror.

        Returns
        -------
        float
            Main mirror area. Given in m^2.

        """

        # Call a sub-module that requires the radius as an input
        return solary.general.geometry.circle_area(self.main_mirror_dia / 2.0)


    @property
    def sec_mirror_area(self) -> float:
        """
        Get the secondary mirror area, assuming a circular shaped mirror.

        Returns
        -------
        float
            Secondary mirror area. Given in m^2.

        """

        # Call a sub-module that requires the radius as an input
        return solary.general.geometry.circle_area(self.sec_mirror_dia / 2.0)


    @property
    def collect_area(self) -> float:
        """
        Get the photon collection area. This propery simply substracts the secondary mirror area
        from the main one.

        Returns
        -------
        float
            Photon collection area. Given in m^2.

        """

        return self.main_mirror_area - self.sec_mirror_area
