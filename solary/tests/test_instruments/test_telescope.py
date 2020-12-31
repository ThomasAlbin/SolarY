"""
TBD

"""

# Import standard libraries
import math

# Import installed libraries
import pytest

# Import solary
import solary


@pytest.fixture
def telescope_test_properties():

    test_paths_config = solary.auxiliary.config.get_paths(test=True)    

    test_reflector_path = \
        solary.auxiliary.parse.get_test_file_path(
            test_paths_config['instruments_optics_reflector']['properties'])

    test_reflector = solary.instruments.optics.read_reflector_config(test_reflector_path)
    
    test_ccd_path = \
        solary.auxiliary.parse.get_test_file_path(
            test_paths_config['instruments_camera_ccd']['properties'])

    test_ccd = solary.instruments.camera.read_ccd_config(test_ccd_path)

    return test_reflector, test_ccd

def test_comp_fov():
    
    fov1 = solary.instruments.telescope.comp_fov(sensor_dim=25.4, 
                                                 focal_length=1000.0)
    
    assert pytest.approx(fov1 / 60.0, abs=0.1) == 87.3

def test_Optical(telescope_test_properties):
    
    test_reflector_config, test_ccd_config = telescope_test_properties
    
    test_telescope = solary.instruments.telescope.ReflectorCCD(test_reflector_config, 
                                                               test_ccd_config)
    
    assert test_telescope.pixels == test_ccd_config['pixels']
    assert test_telescope.main_mirror_dia == test_reflector_config['main_mirror_dia']
    
    # test now the telescope specific properties
    assert pytest.approx(test_telescope.fov[0], abs=0.1) == 1266.8
    assert pytest.approx(test_telescope.fov[1], abs=0.1) == 1271.8
    
    assert test_telescope.ifov[0] == \
               test_telescope.fov[0] / test_telescope.pixels[0]

    assert test_telescope.ifov[1] == \
               test_telescope.fov[1] / test_telescope.pixels[1]

    # set aperture in arcseconds
    test_telescope.aperture = 10.0
    assert test_telescope.aperture == 10.0
    
    # set half flux diameter
    test_telescope.hfdia = 10.0
    assert test_telescope.hfdia == 10.0
    
    # check how many pixels are aperture
    assert test_telescope.pixels_in_aperture == \
        int(round(math.pi * (0.5 * test_telescope.aperture) ** 2.0 / math.prod(test_telescope.ifov), 0))

    # set exposure time in seconds
    test_telescope.exposure_time = 60.0
    assert test_telescope.exposure_time == 60.0