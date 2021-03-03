# pylint: disable=no-member
"""
test_optics.py

Testing suite for solary/instruments/optics.py

"""

# Import installed libraries
import pytest

# Import solary
import SolarY


# Define a test fixture that is being used in all tests. The fixture loads configuration files.
@pytest.fixture(name="reflector_test_optics")
def fixture_reflector_test_optics():
    """
    Fixture to load the test configuration files.

    Returns
    -------
    test_reflector_obj : solary.instruments.optics.Reflector
        Reflector object.

    """

    # Get the test config file paths
    test_paths_config = SolarY.auxiliary.config.get_paths(test=True)

    # Get the path to the relfector config file
    test_reflector_path = SolarY.auxiliary.parse.get_test_file_path(
        "../" + test_paths_config["instruments_optics_reflector"]["properties"]
    )

    # Read and parse the reflector config file and return a dictionary with the properties
    test_reflector_obj = SolarY.instruments.optics.Reflector.load_from_json_file(
        test_reflector_path
    )

    return test_reflector_obj


def test_read_optical_config(reflector_test_optics):
    """
    Testing if the config file reading was successful.

    Parameters
    ----------
    reflector_test_optics : solary.instruments.optics.Reflector
        Reflector object.

    Returns
    -------
    None.

    """

    # Check if the fixture load is a dictionary
    assert isinstance(reflector_test_optics, SolarY.instruments.optics.Reflector)

    # Check the main mirror entry
    assert reflector_test_optics.main_mirror_dia == 1.0


def test_reflector(reflector_test_optics):
    """
    Testing the Reflector Class.

    Parameters
    ----------
    reflector_test_optics : solary.instruments.optics.Reflector
        Reflector object.

    Returns
    -------
    None.

    """

    # Initiate the Reflector class
    # test_reflector_class = solary.instruments.optics.Reflector(reflector_test_optics)

    # Check if the instances of the class correspond to the config file
    assert reflector_test_optics.main_mirror_dia == 1.0
    assert reflector_test_optics.sec_mirror_dia == 0.2
    assert reflector_test_optics.optical_throughput == 0.6
    assert reflector_test_optics.focal_length == 10.0

    # Check the main mirror area that depends on the diameter of the main mirror
    assert (
        reflector_test_optics.main_mirror_area
        == SolarY.general.geometry.circle_area(
            radius=reflector_test_optics.main_mirror_dia / 2.0
        )
    )

    # Check the secondary mirror area that depends on the diameter of the secondary mirror
    assert reflector_test_optics.sec_mirror_area == SolarY.general.geometry.circle_area(
        radius=reflector_test_optics.sec_mirror_dia / 2.0
    )

    # Check now the total collect area
    assert (
        reflector_test_optics.collect_area
        == reflector_test_optics.main_mirror_area
        - reflector_test_optics.sec_mirror_area
    )
