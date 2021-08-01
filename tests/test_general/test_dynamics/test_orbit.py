"""Testing suite for SolarY/general/dyanmics/orbit.py"""
import math

import pytest

import SolarY


@pytest.fixture(name="test_orbit_data")
def fixture_test_orbit_data():
    """
    Fixture to load orbit example data.

    Returns
    -------
    test_orbit_values : dict
        Dictionary that contains the values.
    test_orbit_units : dict
        Dictionary that contains the units.

    """

    # Get the test config file paths
    test_paths_config = SolarY.auxiliary.config.get_paths(test=True)

    test_orbit_path = SolarY.auxiliary.parse.get_test_file_path(
        "../" + test_paths_config["general_astrodyn"]["base_class_orbit"]
    )

    test_orbit_values, test_orbit_units = SolarY.auxiliary.reader.read_orbit(
        test_orbit_path
    )
    
    constant_config = SolarY.auxiliary.config.get_constants()
    one_au_in_km = float(constant_config['constants']['one_au'])

    test_orbit_values['peri'] = test_orbit_values['peri'] * one_au_in_km
    test_orbit_values['incl'] = math.radians(test_orbit_values['incl'])
    test_orbit_values['long_asc_node'] = math.radians(test_orbit_values['long_asc_node'])
    test_orbit_values['arg_peri'] = math.radians(test_orbit_values['arg_peri'])

    return test_orbit_values, test_orbit_units

def test_orbit(test_orbit_data):
    
    test_orbit_values, _ = test_orbit_data
    
    constant_config = SolarY.auxiliary.config.get_constants()
    
    sun_grav_param = float(constant_config['constants']['gm_sun'])
    one_au_in_km = float(constant_config['constants']['one_au'])

    assert sun_grav_param >= 1.30e+11
    
    orbit_class = SolarY.general.dynamics.orbit.Orbit(rp=test_orbit_values['peri'],
                                                      ecc=test_orbit_values['ecc'],
                                                      inc=test_orbit_values['incl'],
                                                      lnode=test_orbit_values['long_asc_node'],
                                                      argp=test_orbit_values['arg_peri'],
                                                      ref='ECLIPJ2000',
                                                      center='SSB',
                                                      grav_param=sun_grav_param)
    
    assert orbit_class.rp == test_orbit_values['peri']
    assert orbit_class.ecc == test_orbit_values['ecc']
    assert orbit_class.inc == test_orbit_values['incl']
    assert orbit_class.lnode == test_orbit_values['long_asc_node']
    assert orbit_class.argp == test_orbit_values['arg_peri']
    
    assert orbit_class.ref == 'ECLIPJ2000'
    assert orbit_class.center == 'SSB'
    assert orbit_class.grav_param == sun_grav_param
    
    assert orbit_class.semi_maj_axis == test_orbit_values['peri'] / (1.0 - test_orbit_values['ecc'])
    assert orbit_class.apo == (1.0 + test_orbit_values['ecc']) * orbit_class.semi_maj_axis
    
    assert orbit_class.center_id == 0
    
def test_state(test_orbit_data):

    test_orbit_values, _ = test_orbit_data    

    constant_config = SolarY.auxiliary.config.get_constants()
    
    sun_grav_param = float(constant_config['constants']['gm_sun'])
        
    orbit_class = SolarY.general.dynamics.orbit.Orbit(rp=test_orbit_values['peri'],
                                                      ecc=test_orbit_values['ecc'],
                                                      inc=test_orbit_values['incl'],
                                                      lnode=test_orbit_values['long_asc_node'],
                                                      argp=test_orbit_values['arg_peri'],
                                                      ref='ECLIPJ2000',
                                                      center='SSB',
                                                      grav_param=sun_grav_param)    

    state_class = SolarY.general.dynamics.orbit.State(orbit=orbit_class,
                                                      m0=math.radians(77.4),
                                                      t0="2019-04-27T00:00:00",
                                                      et="2021-08-01T12:00:00")

    assert state_class.orbit.rp == test_orbit_values['peri']

    assert state_class.m0 == math.radians(77.4)
    state_class.m0 = math.radians(77.4)
    assert state_class.m0 == math.radians(77.4)

    state_class.t0 = "2019-04-27T00:00:00"
    assert state_class.t0 == "2019-04-27T00:00:00"
    assert state_class.t0_ephem == 609595269.1855328

    state_class.et = "2021-08-01T12:00:00"
    assert state_class.et == "2021-08-01T12:00:00"
    assert state_class.et_ephem == 681091269.1832587

    ceres_state_exp = [320385504.0, 274563074.0, -50443815.0,
                       -11.9, 12.5, 2.6]

    assert all([pytest.approx(comp, 0.1) == exp for comp, exp \
                in zip(state_class.state_vec, ceres_state_exp)])