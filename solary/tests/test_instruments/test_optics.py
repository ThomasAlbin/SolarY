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
def reflector_test_optics():
    
    test_paths_config = solary.auxiliary.config.get_paths(test=True)

    test_reflector_path = \
        solary.auxiliary.parse.get_test_file_path(
            test_paths_config['instruments_optics_reflector']['properties'])

    test_reflector = solary.instruments.optics.read_reflector_config(test_reflector_path)

    return test_reflector

def test_read_optical_config(reflector_test_optics):
    
    assert reflector_test_optics['main_mirror_dia'] == 1.0

def test_Optical(reflector_test_optics):
    
    test_reflector = solary.instruments.optics.Reflector(reflector_test_optics)
    
    assert test_reflector.main_mirror_dia == reflector_test_optics['main_mirror_dia']
    assert test_reflector.sec_mirror_dia == reflector_test_optics['sec_mirror_dia']
    assert test_reflector.optical_throughput == reflector_test_optics['optical_throughput']
    assert test_reflector.focal_length == reflector_test_optics['focal_length']
    
    # test now the property
    assert test_reflector.main_mirror_area == math.pi \
        * ((reflector_test_optics['main_mirror_dia'] / 2.0) ** 2.0)
        
    assert test_reflector.sec_mirror_area == math.pi \
        * ((reflector_test_optics['sec_mirror_dia'] / 2.0) ** 2.0)
        
    assert test_reflector.collect_area == \
        test_reflector.main_mirror_area - test_reflector.sec_mirror_area