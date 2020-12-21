"""
TBD

"""

# Import installed libraries
import pytest

# Import solary
import solary


@pytest.fixture
def telescope_test_optics():
    
    test_paths_config = solary.auxiliary.config.get_paths(test=True)

    test_optical_path = \
        solary.auxiliary.parse.get_test_file_path(
            test_paths_config['instruments_telescope_optical']['properties'])

    test_optics = solary.instruments.telescope.read_optical_config(test_optical_path)

    return test_optics

def test_read_optical_config(telescope_test_optics):
    
    assert telescope_test_optics['main_mirror_dia'] == 1.0

def test_Optical(telescope_test_optics):
    
    test_telescope = solary.instruments.telescope.Optical(telescope_test_optics)
    
    assert test_telescope.main_mirror_dia == telescope_test_optics['main_mirror_dia']
    assert test_telescope.sec_mirr_dia == telescope_test_optics['sec_mirr_dia']
    assert test_telescope.optical_throughput == telescope_test_optics['optical_throughput']
    assert test_telescope.focal_length == telescope_test_optics['focal_length']