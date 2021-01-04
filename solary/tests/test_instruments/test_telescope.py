# pylint: disable=W0212
"""
test_telescope.py

Testing suite for solary/instruments/telescope.py

"""

# Import standard libraries
import math

# Import installed libraries
import pytest

# Import solary
import solary


@pytest.fixture(name='telescope_test_properties')
def fixture_telescope_test_properties():
    """
    Fixture to load the test configuration files.


    Returns
    -------
    test_reflector : dict
        Reflector test configuration.
    test_ccd : dict
        CCD test configuration.

    """

    # Get the test config paths
    test_paths_config = solary.auxiliary.config.get_paths(test=True)

    # Load and parse the reflector config
    test_reflector_path = \
        solary.auxiliary.parse.get_test_file_path(
            test_paths_config['instruments_optics_reflector']['properties'])

    test_reflector = solary.instruments.optics.read_reflector_config(test_reflector_path)

    # Load and parse the CCD properties
    test_ccd_path = \
        solary.auxiliary.parse.get_test_file_path(
            test_paths_config['instruments_camera_ccd']['properties'])

    test_ccd = solary.instruments.camera.read_ccd_config(test_ccd_path)

    return test_reflector, test_ccd


def test_comp_fov():
    """
    Test the Field-Of-View computation function

    Returns
    -------
    None.

    """

    # Test sample with a sensor dimension / size of 25.4 mm and a telescope focial length of 1000
    # mm
    fov1 = solary.instruments.telescope.comp_fov(sensor_dim=25.4,
                                                 focal_length=1000.0)
    assert pytest.approx(fov1 / 60.0, abs=0.1) == 87.3


def test_reflectorccd(telescope_test_properties):
    """
    Testing the telescope class. To compare the rather complex and error-prone computation, a PERL
    based script from [1] has been used for rough computation comparisons.

    Parameters
    ----------
    telescope_test_properties : tuple
        Tuple with 2 dictionaries: reflector config dict and CCD config dict.

    Returns
    -------
    None.

    References
    ----------
    [1] http://spiff.rit.edu/richmond/signal.shtml 04.Jan.2021

    """

    # Set some settings for later use
    photometric_aperture = 10.0
    half_flux_diameter = 10.0
    expos_time = 60.0

    # Set some observational parameters
    object_brightness = 19.0
    sky_brightness = 19.0

    # Check if the property tuple is correctly formatted
    assert isinstance(telescope_test_properties, tuple)
    assert len(telescope_test_properties) == 2

    # Get the config dictionaries
    test_reflector_config, test_ccd_config = telescope_test_properties

    # Initiate the telescope class
    test_telescope = solary.instruments.telescope.ReflectorCCD(test_reflector_config,
                                                               test_ccd_config)

    # Check attributes
    assert test_telescope.pixels == test_ccd_config['pixels']
    assert test_telescope.main_mirror_dia == test_reflector_config['main_mirror_dia']

    # Test if constants config has been loaded
    config = solary.auxiliary.config.get_constants()
    assert test_telescope._photon_flux_v == float(config['photometry']['photon_flux_V'])

    # Test now the telescope specific properties, FOV
    assert pytest.approx(test_telescope.fov[0], abs=0.1) == 1266.8
    assert pytest.approx(test_telescope.fov[1], abs=0.1) == 1271.8

    # Check iFOV
    assert test_telescope.ifov[0] == test_telescope.fov[0] / test_telescope.pixels[0]

    assert test_telescope.ifov[1] == test_telescope.fov[1] / test_telescope.pixels[1]

    # Set aperture in arcsec
    test_telescope.aperture = photometric_aperture
    assert test_telescope.aperture == photometric_aperture

    # Set the half flux diameter in arcsec
    test_telescope.hfdia = half_flux_diameter
    assert test_telescope.hfdia == half_flux_diameter

    # Check how many pixels are aperture
    assert test_telescope.pixels_in_aperture == \
        int(round(solary.general.geometry.circle_area(0.5 * test_telescope.aperture) \
                  / math.prod(test_telescope.ifov), 0))

    # Set exposure time in seconds
    test_telescope.exposure_time = expos_time
    assert test_telescope.exposure_time == expos_time

    # Compute the light fraction in aperture
    assert test_telescope._ratio_light_aperture == \
        math.erf((test_telescope.aperture) \
                 / (solary.general.geometry.fwhm2std(test_telescope.hfdia)*math.sqrt(2)))**2.0

    # Compute raw object electrons (expectation)
    exp_e_signal = round(10.0 ** (-0.4 * object_brightness) \
                         * float(config['photometry']['photon_flux_V']) \
                         * expos_time \
                         * test_telescope.collect_area \
                         * test_telescope.quantum_eff \
                         * test_telescope.optical_throughput \
                         * test_telescope._ratio_light_aperture, 0)

    # Compute the electron signal and compare the results
    object_electrons_apert = test_telescope.object_esignal(mag=object_brightness)
    assert object_electrons_apert == exp_e_signal

    # Compute sky background signal (expectation)
    # Convert surface brightness to integrated brightness over entire FOV
    total_sky_mag = solary.general.photometry.surmag2intmag(surmag=sky_brightness, \
                                                            area=math.prod(test_telescope.fov))
    exp_sky_esignal = round(10.0 ** (-0.4 * total_sky_mag) \
                            * float(config['photometry']['photon_flux_V']) \
                            * expos_time \
                            * test_telescope.collect_area \
                            * test_telescope.quantum_eff \
                            * test_telescope.optical_throughput \
                            * (test_telescope.pixels_in_aperture
                               / math.prod(test_telescope.pixels)), 0)

    # Compare computation with expectation
    sky_electrons_apert = test_telescope.sky_esignal(mag_arcsec_sq=sky_brightness)
    assert sky_electrons_apert == exp_sky_esignal

    # Test the dark current
    assert test_telescope.dark_esignal_aperture == \
        round(float(test_ccd_config['dark_noise']) \
              * expos_time \
              * test_telescope.pixels_in_aperture, 0)

    # Now test the SNR
    assert pytest.approx(test_telescope.object_snr(obj_mag=object_brightness,
                                                   sky_mag_arcsec_sq=sky_brightness),
                                                   abs=0.1) == 5.0
