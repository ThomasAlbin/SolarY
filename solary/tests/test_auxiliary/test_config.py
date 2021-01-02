"""
test_config.py

Testing suite for solary/auxiliary/config.py

"""

# Import solary
import solary


def test_get_constants():
    """
    Test function to check whether the constants file is read successfully

    Returns
    -------
    None.

    """

    # Call the constants get function
    constant_config = solary.auxiliary.config.get_constants()

    # If the reading was successful the config object shall have miscellaneous sections and
    # corresponding values. One of them is called "constants"
    constant_config_sections = constant_config.sections()
    assert 'constants' in constant_config_sections


def test_get_paths():
    """
    Test function to check whether the path config file is read.

    Returns
    -------
    None.

    """

    # Call the paths config file
    paths_config = solary.auxiliary.config.get_paths()

    # If the reading was successful the config object shall have miscellaneous sections and
    # corresponding values. One of them is called "neo"
    paths_config_sections = paths_config.sections()
    assert 'neo' in paths_config_sections

    # Testing now the test config
    test_paths_config = solary.auxiliary.config.get_paths(test=True)

    # If the reading was successful the config object shall have miscellaneous sections and
    # corresponding values. One of them contains "instruments_telescope_optical"
    test_paths_config_sections = test_paths_config.sections()
    assert 'instruments_optics_reflector' in test_paths_config_sections
