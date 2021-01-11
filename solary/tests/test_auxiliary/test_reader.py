"""
test_reader.py

Testing suite for the reader functionality

"""

# Import SolarY
import solary


def test_read_orbit():
    """
    Test the reader function read_orbit.

    Returns
    -------
    None.

    """

    # Get the test config file paths
    test_paths_config = solary.auxiliary.config.get_paths(test=True)

    # Parse the orbit path
    test_orbit_path = \
        solary.auxiliary.parse.get_test_file_path(
            test_paths_config['general_astrodyn']['base_class_orbit'])

    # Read and parse the orbit file and return a values and units dictionary
    test_orbit_values, test_orbit_units = \
        solary.auxiliary.reader.read_orbit(test_orbit_path)

    # Check whether the instances are correct and the expectations
    assert isinstance(test_orbit_values, dict)
    assert isinstance(test_orbit_units, dict)

    assert test_orbit_values['peri'] == 1.133
    assert test_orbit_units['spatial'] == 'AU'
