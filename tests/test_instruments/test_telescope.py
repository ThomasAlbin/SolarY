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


@pytest.fixture(name="telescope_test_obj")
def fixture_telescope_test_obj():
    """
    Fixture to load the test configuration files.


    Returns
    -------
    test_reflector_ccd : solary.instruments.telescope.ReflectorCCD
        Reflector test object.

    """

    # Get the test config paths
    test_paths_config = solary.auxiliary.config.get_paths(test=True)

    # Load and parse the reflector config
    test_reflector_path = solary.auxiliary.parse.get_test_file_path(
        "../" + test_paths_config["instruments_optics_reflector"]["properties"]
    )

    test_reflector = solary.instruments.optics.Reflector.load_from_json_file(
        test_reflector_path
    )

    # Load and parse the CCD properties
    test_ccd_path = solary.auxiliary.parse.get_test_file_path(
        "../" + test_paths_config["instruments_camera_ccd"]["properties"]
    )

    test_ccd = solary.instruments.camera.CCD.load_from_json_file(test_ccd_path)

    test_reflector_ccd = solary.instruments.telescope.ReflectorCCD.load_from_json_file(
        optics_path=test_reflector_path,
        ccd_path=test_ccd_path,
    )
    return test_reflector_ccd


def test_comp_fov():
    """
    Test the Field-Of-View computation function

    Returns
    -------
    None.

    """

    # Test sample with a sensor dimension / size of 25.4 mm and a telescope focial length of 1000
    # mm
    fov1 = solary.instruments.telescope.comp_fov(sensor_dim=25.4, focal_length=1000.0)
    assert pytest.approx(fov1 / 60.0, abs=0.1) == 87.3


def test_reflectorccd(telescope_test_obj):
    """
    Testing the telescope class. To compare the rather complex and error-prone computation, a PERL
    based script from [1] has been used for rough computation comparisons.

    Parameters
    ----------
    test_reflector_ccd : solary.instruments.telescope.ReflectorCCD
        Reflector test object.

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
    assert isinstance(telescope_test_obj, solary.instruments.telescope.ReflectorCCD)

    # Check attributes
    assert telescope_test_obj.pixels == telescope_test_obj.pixels
    assert telescope_test_obj.main_mirror_dia == telescope_test_obj.main_mirror_dia

    # Test if constants config has been loaded
    config = solary.auxiliary.config.get_constants()
    assert telescope_test_obj._photon_flux_v == float(config["photometry"]["photon_flux_V"])

    # Test now the telescope specific properties, FOV
    assert pytest.approx(telescope_test_obj.fov[0], abs=0.1) == 1266.8
    assert pytest.approx(telescope_test_obj.fov[1], abs=0.1) == 1271.8

    # Check iFOV
    assert telescope_test_obj.ifov[0] == telescope_test_obj.fov[0] / telescope_test_obj.pixels[0]

    assert telescope_test_obj.ifov[1] == telescope_test_obj.fov[1] / telescope_test_obj.pixels[1]

    # Set aperture in arcsec
    telescope_test_obj.aperture = photometric_aperture
    assert telescope_test_obj.aperture == photometric_aperture

    # Set the half flux diameter in arcsec
    telescope_test_obj.hfdia = half_flux_diameter
    assert telescope_test_obj.hfdia == half_flux_diameter

    # Check how many pixels are aperture
    assert telescope_test_obj.pixels_in_aperture == int(
        round(
            solary.general.geometry.circle_area(0.5 * telescope_test_obj.aperture)
            / math.prod(telescope_test_obj.ifov),
            0,
        )
    )

    # Set exposure time in seconds
    telescope_test_obj.exposure_time = expos_time
    assert telescope_test_obj.exposure_time == expos_time

    # Compute the light fraction in aperture
    assert (
            telescope_test_obj._ratio_light_aperture
        == math.erf(
            (telescope_test_obj.aperture)
            / (solary.general.geometry.fwhm2std(telescope_test_obj.hfdia) * math.sqrt(2))
        )
        ** 2.0
    )

    # Compute raw object electrons (expectation)
    exp_e_signal = round(
        10.0 ** (-0.4 * object_brightness)
        * float(config["photometry"]["photon_flux_V"])
        * expos_time
        * telescope_test_obj.collect_area
        * telescope_test_obj.quantum_eff
        * telescope_test_obj.optical_throughput
        * telescope_test_obj._ratio_light_aperture,
        0,
    )

    # Compute the electron signal and compare the results
    object_electrons_apert = telescope_test_obj.object_esignal(mag=object_brightness)
    assert object_electrons_apert == exp_e_signal

    # Compute sky background signal (expectation)
    # Convert surface brightness to integrated brightness over entire FOV
    total_sky_mag = solary.general.photometry.surmag2intmag(
        surmag=sky_brightness, area=math.prod(telescope_test_obj.fov)
    )
    exp_sky_esignal = round(
        10.0 ** (-0.4 * total_sky_mag)
        * float(config["photometry"]["photon_flux_V"])
        * expos_time
        * telescope_test_obj.collect_area
        * telescope_test_obj.quantum_eff
        * telescope_test_obj.optical_throughput
        * (telescope_test_obj.pixels_in_aperture / math.prod(telescope_test_obj.pixels)),
        0,
    )

    # Compare computation with expectation
    sky_electrons_apert = telescope_test_obj.sky_esignal(mag_arcsec_sq=sky_brightness)
    assert sky_electrons_apert == exp_sky_esignal

    # Test the dark current
    assert telescope_test_obj.dark_esignal_aperture == round(
        float(telescope_test_obj.dark_noise)
        * expos_time
        * telescope_test_obj.pixels_in_aperture,
        0,
    )

    # Now test the SNR
    assert (
        pytest.approx(
            telescope_test_obj.object_snr(
                obj_mag=object_brightness, sky_mag_arcsec_sq=sky_brightness
            ),
            abs=0.1,
        )
        == 5.0
    )
