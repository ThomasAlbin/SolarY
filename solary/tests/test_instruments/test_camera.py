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
def ccd_test_optics():
    
    test_paths_config = solary.auxiliary.config.get_paths(test=True)

    test_ccd_path = \
        solary.auxiliary.parse.get_test_file_path(
            test_paths_config['instruments_camera_ccd']['properties'])

    test_ccd = solary.instruments.camera.read_ccd_config(test_ccd_path)

    return test_ccd

def test_read_ccd_config(ccd_test_optics):
    
    assert ccd_test_optics['pixels'] == [4096, 4112]

def test_Optical(ccd_test_optics):
    
    test_ccd = solary.instruments.camera.CCD(ccd_test_optics)
    
    assert test_ccd.pixels == ccd_test_optics['pixels']
    assert test_ccd.pixel_size == ccd_test_optics['pixel_size']
    assert test_ccd.dark_noise == ccd_test_optics['dark_noise']
    assert test_ccd.readout_noise == ccd_test_optics['readout_noise']
    assert test_ccd.full_well == ccd_test_optics['full_well']

    # test now the chip size
    assert test_ccd.chip_size[0] == \
        ccd_test_optics['pixels'][0] * ccd_test_optics['pixel_size'] / 1000.0
        
#     assert test_telescope.sec_mirror_area == math.pi \
#         * ((telescope_test_optics['sec_mirror_dia'] / 2.0) ** 2.0)
        
#     assert test_telescope.collect_area == \
#         test_telescope.main_mirror_area - test_telescope.sec_mirror_area