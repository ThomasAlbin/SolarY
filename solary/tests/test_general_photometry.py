import configparser
import math

import pytest
import solary

def test_appmag2irr():

    config = configparser.ConfigParser()
    config.read('_config/constants.ini')
    appmag_irr_i0 = float(config['photometry']['appmag_irr_i0'])

    irradiance1 = solary.general.photometry.appmag2irr(app_mag=0)
    assert pytest.approx(irradiance1) == appmag_irr_i0

    irradiance2 = solary.general.photometry.appmag2irr(app_mag=-5)
    assert pytest.approx(irradiance2) == appmag_irr_i0 * 100.0

    irradiance3 = solary.general.photometry.appmag2irr(app_mag=1)
    assert pytest.approx(irradiance3) == 1.0024422165005002e-08

def test_phase_func():
    
    phi1_res1 = solary.general.photometry.phase_func(index=1, phase_angle=0.0)
    assert phi1_res1 == 1.0
    
    phi2_res1 = solary.general.photometry.phase_func(index=1, phase_angle=0.0)
    assert phi2_res1 == 1.0

    phi1_res2 = solary.general.photometry.phase_func(index=1, phase_angle=math.pi/2.0)
    assert phi1_res2 == 0.03579310506765532
    
    phi2_res2 = solary.general.photometry.phase_func(index=2, phase_angle=math.pi/2.0)
    assert phi2_res2 == 0.15412366181513143