"""
test_camera.py

Testing suite for solary/instruments/camera.py

"""

# Import installed libraries
import pytest

# Import solary
import solary


# Define a test fixture that is being used in all tests. The fixture loads configuration files.
@pytest.fixture(name='ccd_test_config')
def fixture_ccd_test_config():
    """
    Fixture to load the test configuration files.

    Returns
    -------
    test_ccd_dict : dict
        CCD test configuration.

    """

    # Get the test config file paths
    test_paths_config = solary.auxiliary.config.get_paths(test=True)

    # Get the path to the CCD config file
    test_ccd_path = \
        solary.auxiliary.parse.get_test_file_path(
            test_paths_config['instruments_camera_ccd']['properties'])

    # Read and parse the CCD config file and return a dictionary with the properties
    test_ccd_dict = solary.instruments.camera.read_ccd_config(test_ccd_path)

    return test_ccd_dict


def test_read_ccd_config(ccd_test_config):
    """
    Testing if the config file reading was successful.

    Parameters
    ----------
    ccd_test_config : dict
        CCD config dictionary.

    Returns
    -------
    None.

    """

    # Check if the fixture load is a dictionary
    assert isinstance(ccd_test_config, dict)

    # Check the pixels
    assert ccd_test_config['pixels'] == [4096, 4112]

def test_ccd(ccd_test_config):
    """
    Testing the CCD Class.

    Parameters
    ----------
    ccd_test_config : dict
        CCD config dictionary.

    Returns
    -------
    None.

    """

    # Initiate the CCD class
    test_ccd_class = solary.instruments.camera.CCD(ccd_test_config)

    # Check the config depending attributes
    assert test_ccd_class.pixels == ccd_test_config['pixels']
    assert test_ccd_class.pixel_size == ccd_test_config['pixel_size']
    assert test_ccd_class.dark_noise == ccd_test_config['dark_noise']
    assert test_ccd_class.readout_noise == ccd_test_config['readout_noise']
    assert test_ccd_class.full_well == ccd_test_config['full_well']
    assert test_ccd_class.quantum_eff == ccd_test_config['quantum_eff']

    # Check the first entry of the chip size. Multiply the number of pixels (x dimension) times the
    # pixel size in micro meters. Finally divide by 1000 to get a result in mm.
    assert test_ccd_class.chip_size[0] == ccd_test_config['pixels'][0] \
                                          * ccd_test_config['pixel_size'] / 1000.0

    # Check the size of a single pixel in m^2. The pixel size squared leads to micro meter squared.
    # Divide the results by 10^-12.
    assert test_ccd_class.pixel_size_sq_m == (ccd_test_config['pixel_size'] ** 2.0) \
                                             * 10.0 ** (-12.0)
