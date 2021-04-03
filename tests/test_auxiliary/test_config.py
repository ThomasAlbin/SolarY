"""
test_config.py

Testing suite for SolarY/auxiliary/config.py

"""
import SolarY


def test_get_constants():
    """
    Test function to check whether the constants file is read successfully

    Returns
    -------
    None.

    """

    # Call the constants get function
    constant_config = SolarY.auxiliary.config.get_constants()

    # If the reading was successful the config object shall have miscellaneous sections and
    # corresponding values. One of them is called "constants"
    constant_config_sections = constant_config.sections()
    assert "constants" in constant_config_sections


def test_get_paths():
    """
    Test function to check whether the path config file is read.

    Returns
    -------
    None.

    """

    # Call the paths config file
    paths_config = SolarY.auxiliary.config.get_paths()

    # If the reading was successful the config object shall have miscellaneous sections and
    # corresponding values. One of them is called "neo"
    paths_config_sections = paths_config.sections()
    assert "neo" in paths_config_sections

    # Testing now the test config
    test_paths_config = SolarY.auxiliary.config.get_paths(test=True)

    # If the reading was successful the config object shall have miscellaneous sections and
    # corresponding values. One of them contains "instruments_telescope_optical"
    test_paths_config_sections = test_paths_config.sections()
    assert "instruments_optics_reflector" in test_paths_config_sections


def test_get_spice_kernels():
    """
    Test function to check the correct parsinf of the SPICE config file.

    Returns
    -------
    None.

    """

    # Call the paths config file
    paths_config = SolarY.auxiliary.config.get_spice_kernels(ktype="generic")

    # If the reading was successful the config object shall have miscellaneous sections and
    # corresponding values. One of them is called "leapseconds".  Further, "file" shall always
    # be present in a section.
    paths_config_sections = paths_config.sections()
    assert "leapseconds" in paths_config_sections
    assert "file" in paths_config["leapseconds"].keys()


def test_load_spice_kernels():
    """
    Test function to chek the correct loading of SPICE kernels

    Returns
    -------
    None.
    """

    # Load the generic kernels. If all kernels are present no error should
    # occur
    SolarY.auxiliary.config.load_spice_kernels(ktype="generic")
