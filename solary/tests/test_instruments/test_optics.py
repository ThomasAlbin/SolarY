# pylint: disable=no-member
"""
test_optics.py

Testing suite for solary/instruments/optics.py

"""

# Import installed libraries
import pytest

# Import solary
import solary


# Define a test fixture that is being used in all tests. The fixture loads configuration files.
@pytest.fixture(name='reflector_test_optics')
def fixture_reflector_test_optics():
    """
    Fixture to load the test configuration files.

    Returns
    -------
    test_reflector_dict : dict
        Reflector test configuration.

    """

    # Get the test config file paths
    test_paths_config = solary.auxiliary.config.get_paths(test=True)

    # Get the path to the relfector config file
    test_reflector_path = \
        solary.auxiliary.parse.get_test_file_path(
            test_paths_config['instruments_optics_reflector']['properties'])

    # Read and parse the reflector config file and return a dictionary with the properties
    test_reflector_dict = solary.instruments.optics.read_reflector_config(test_reflector_path)

    return test_reflector_dict


def test_read_optical_config(reflector_test_optics):
    """
    Testing if the config file reading was successful.

    Parameters
    ----------
    reflector_test_optics : dict
        Reflector config dictionary.

    Returns
    -------
    None.

    """

    # Check if the fixture load is a dictionary
    assert isinstance(reflector_test_optics, dict)

    # Check the main mirror entry
    assert reflector_test_optics['main_mirror_dia'] == 1.0


def test_reflector(reflector_test_optics):
    """
    Testing the Reflector Class.

    Parameters
    ----------
    reflector_test_optics : dict
        Reflector config dictionary.

    Returns
    -------
    None.

    """

    # Initiate the Reflector class
    test_reflector_class = solary.instruments.optics.Reflector(reflector_test_optics)

    # Check if the instances of the class correspond to the config file
    assert test_reflector_class.main_mirror_dia == reflector_test_optics['main_mirror_dia']
    assert test_reflector_class.sec_mirror_dia == reflector_test_optics['sec_mirror_dia']
    assert test_reflector_class.optical_throughput == reflector_test_optics['optical_throughput']
    assert test_reflector_class.focal_length == reflector_test_optics['focal_length']

    # Check the main mirror area that depends on the diameter of the main mirror
    assert test_reflector_class.main_mirror_area == \
        solary.general.geometry.circle_area(radius=reflector_test_optics['main_mirror_dia'] / 2.0)

    # Check the secondary mirror area that depends on the diameter of the secondary mirror
    assert test_reflector_class.sec_mirror_area == \
        solary.general.geometry.circle_area(radius=reflector_test_optics['sec_mirror_dia'] / 2.0)

    # Check now the total collect area
    assert test_reflector_class.collect_area == \
        test_reflector_class.main_mirror_area - test_reflector_class.sec_mirror_area
