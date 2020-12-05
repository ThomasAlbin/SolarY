import configparser
import math
import os

import pytest
import solary

def test_tisserand():
    
    tisserand_parameter1 = solary.general.astrodyn.tisserand(sem_maj_axis_obj=5.0, \
                                                             inc=0.0, \
                                                             ecc=0.0)
    assert tisserand_parameter1 == 3.001200087241328

    tisserand_parameter2 = solary.general.astrodyn.tisserand(sem_maj_axis_obj=4.0, \
                                                             inc=0.0, \
                                                             ecc=0.65)
    assert tisserand_parameter2 == 2.633422691976387
    
    tisserand_parameter3 = solary.general.astrodyn.tisserand(sem_maj_axis_obj=4.0, \
                                                             inc=math.radians(30.0), \
                                                             ecc=0.65)
    assert tisserand_parameter3 == 2.454890564710888

    tisserand_parameter4 = solary.general.astrodyn.tisserand(sem_maj_axis_obj=4.0, \
                                                             inc=math.radians(30.0), \
                                                             ecc=0.65, \
                                                             sem_maj_axis_planet=3.0)
    assert tisserand_parameter4 == 2.2698684153570663

def test_kep_apoapsis():
    
    apoapsis1 = solary.general.astrodyn.kep_apoapsis(sem_maj_axis=5.0, ecc=0.3)
    assert apoapsis1 == 6.5

    apoapsis2 = solary.general.astrodyn.kep_apoapsis(sem_maj_axis=10.0, ecc=0.0)
    assert apoapsis2 == 10

def test_kep_periapsis():
    
    periapsis1 = solary.general.astrodyn.kep_periapsis(sem_maj_axis=5.0, ecc=0.3)
    assert periapsis1 == 3.5

    periapsis2 = solary.general.astrodyn.kep_periapsis(sem_maj_axis=10.0, ecc=0.0)
    assert periapsis2 == 10

def test_mjd2jd():
    
    jd1 = solary.general.astrodyn.mjd2jd(m_juldate=56123.5)
    assert jd1 == 2456124

def test_jd2mjd():
    
    mjd1 = solary.general.astrodyn.jd2mjd(juldate=2456000.5)
    assert mjd1 == 56000.0

def test_sphere_of_influence():

    # Set config parser
    config = configparser.ConfigParser()

    # Find the constants.ini
    module_path = os.path.dirname(__file__)
    constants_ini_path = os.path.join(module_path, '../..', '_config', 'constants.ini')

    # Read and parse the config file
    config.read(constants_ini_path)
    sem_maj_axis_earth = float(config['constants']['one_au'])
    
    grav_const = float(config['constants']['grav_const'])
    
    earth_mass = float(config['constants']['gm_earth']) / grav_const  
    sun_mass = float(config['constants']['gm_sun']) / grav_const



    soi_res_earth = solary.general.astrodyn.sphere_of_influence(sem_maj_axis=sem_maj_axis_earth, \
                                                                minor_mass=earth_mass, \
                                                                major_mass=sun_mass)
    assert pytest.approx(soi_res_earth, abs=1e4) == 925000.0