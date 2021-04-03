"""Auxiliary functions for all library relevant configuration files."""
import configparser
import importlib
import os

import spiceypy

from .. import auxiliary as solary_auxiliary

root_dir = os.path.dirname(importlib.import_module("SolarY").__file__)


def get_constants() -> configparser.ConfigParser:
    """
    Get the constants.ini file from the _config directory.

    Returns
    -------
    config : configparser.ConfigParser
        Configuration Parser that contains miscellaneous constants (like astrodynmical, time,
        etc.)
    """
    # Set config parser
    config = configparser.ConfigParser()

    # Get the constants ini file
    constants_ini_path = os.path.join(root_dir, "_config", "constants.ini")

    # Read and parse the config file
    config.read(constants_ini_path)

    return config


def get_paths(test: bool = False) -> configparser.ConfigParser:
    """
    Get the ``paths.dir`` file from the _config directory.

    Parameters
    ----------
    test : bool
        Boolean value whether to use the default (prod.) or test configs. Default: False

    Returns
    -------
    config : configparser.ConfigParser
        Configuration Parser that contains miscellaneous paths to store / access / etc. downloaded
        files, created database etc.
    """
    # Set the config parser
    config = configparser.ConfigParser()

    # Get the paths ini file, differentiate between prod and test
    if test:
        paths_ini_path = os.path.join(
            root_dir, "../", "tests/_resources/_config", "test_paths.ini"
        )
    else:
        paths_ini_path = os.path.join(root_dir, "_config", "paths.ini")

    # Read and parse the config file
    config.read(paths_ini_path)

    return config


def get_spice_kernels(ktype: str) -> configparser.ConfigParser:
    """
    Get the kernel information from the _config directory.

    Parameters
    ----------
    ktype : str
        SPICE Kernel type (e.g., "generic").

    Returns
    -------
    config : configparser.ConfigParser
        Configuration Parser that contains miscellaneous kernel information like the URL, type,
        directory and filename.
    """
    # Set the config parser
    config = configparser.ConfigParser()

    # Current kernel dictionary that encodes the present config files
    kernel_dict = {"generic": "generic.ini"}

    # Get the corresponding kernel config filepath
    ini_path = os.path.join(root_dir, "_config", "SPICE", kernel_dict.get(ktype, ""))

    # Read and parse the config file
    config.read(ini_path)

    return config


def load_spice_kernels(ktype: str):
    """
    Load SPICE kernels.

    Depending on the requests kernel type input the corresponding kernels are loaded. If files are
    not present they will be downloaded automatically into the home directory.

    Parameters
    ----------
    ktype : str
        DESCRIPTION.

    Returns
    -------
    None.

    """

    # Get the kernel file
    kernel_config = get_spice_kernels(ktype=ktype)

    # Try to parse and load the files
    try:

        # Iterate through all kernel sections
        for kernel_t in kernel_config.sections():

            # Extract directory and filename of the kernel file and aprse the filepath
            path_t = kernel_config[kernel_t]["dir"]
            file_t = kernel_config[kernel_t]["file"]
            filepath_t = solary_auxiliary.parse.setnget_file_path(dl_path=path_t, filename=file_t)

            # Load the kernel
            spiceypy.furnsh(filepath_t)

    # Exception: download the SPICE kernels if they have not been found (currently only generic
    # ones)
    except spiceypy.utils.exceptions.SpiceNOSUCHFILE:
        solary_auxiliary.download.spice_generic_kernels()
