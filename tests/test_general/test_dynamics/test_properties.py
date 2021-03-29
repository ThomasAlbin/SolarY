"""Testing suite for SolarY/general/dyanmics/properties.py"""
import math

import pytest

import SolarY

def test_tisserand():
    """
    Test function for the Tisserand computation function.

    Returns
    -------
    None.

    """

    # Compute Tisserand parameter (test case #1) and compare with expectation
    tisserand_parameter1 = SolarY.general.dynamics.properties.tisserand(
        sem_maj_axis_obj=5.0, inc=0.0, ecc=0.0
    )
    assert tisserand_parameter1 == 3.001200087241328

    # Compute Tisserand parameter (test case #2) and compare with expectation
    tisserand_parameter2 = SolarY.general.dynamics.properties.tisserand(
        sem_maj_axis_obj=4.0, inc=0.0, ecc=0.65
    )
    assert tisserand_parameter2 == 2.633422691976387

    # Compute Tisserand parameter (test case #3) and compare with expectation
    tisserand_parameter3 = SolarY.general.dynamics.properties.tisserand(
        sem_maj_axis_obj=4.0, inc=math.radians(30.0), ecc=0.65
    )
    assert tisserand_parameter3 == 2.454890564710888

    # Compute Tisserand parameter (test case #4) and compare with expectation
    tisserand_parameter4 = SolarY.general.dynamics.properties.tisserand(
        sem_maj_axis_obj=4.0, inc=math.radians(30.0), ecc=0.65, sem_maj_axis_planet=3.0
    )
    assert tisserand_parameter4 == 2.2698684153570663


def test_kep_apoapsis():
    """
    Test function for the Apoapsis computation.

    Returns
    -------
    None.

    """

    # Compute the Apoapsis and perform assertion test (example #1)
    apoapsis1 = SolarY.general.dynamics.properties.kep_apoapsis(sem_maj_axis=5.0, ecc=0.3)
    assert apoapsis1 == 6.5

    # Compute the Apoapsis and perform assertion test (example #2)
    apoapsis2 = SolarY.general.dynamics.properties.kep_apoapsis(sem_maj_axis=10.0, ecc=0.0)
    assert apoapsis2 == 10


def test_kep_periapsis():
    """
    Test function for the Periapsis computation.

    Returns
    -------
    None.

    """

    # Compute the Periapsis and perform assertion test (example #1)
    periapsis1 = SolarY.general.dynamics.properties.kep_periapsis(sem_maj_axis=5.0, ecc=0.3)
    assert periapsis1 == 3.5

    # Compute the Periapsis and perform assertion test (example #2)
    periapsis2 = SolarY.general.dynamics.properties.kep_periapsis(sem_maj_axis=10.0, ecc=0.0)
    assert periapsis2 == 10


def test_mjd2jd():
    """
    Test function to verify Modified Julian Date to Julian Date converter function.

    Returns
    -------
    None.

    """

    # Compute the JD with a given MJD
    jd1 = SolarY.general.dynamics.properties.mjd2jd(m_juldate=56123.5)
    assert jd1 == 2456124


def test_jd2mjd():
    """
    Test function to verify Julian Date to Modified Julian Date converter function.

    Returns
    -------
    None.

    """

    # Compute the MJD with a given JD
    mjd1 = SolarY.general.dynamics.properties.jd2mjd(juldate=2456000.5)
    assert mjd1 == 56000.0


def test_sphere_of_influence():
    """
    Test function to check the Sphere Of Influence (SOI) computation function.

    Returns
    -------
    None.

    """

    # Read the constants config file and get the value for 1 AU, grav. constant, Earth's and Sun's
    # grav. constant (and convert both to mass)
    config = SolarY.auxiliary.config.get_constants()
    sem_maj_axis_earth = float(config["constants"]["one_au"])
    grav_const = float(config["constants"]["grav_const"])
    earth_mass = float(config["constants"]["gm_earth"]) / grav_const
    sun_mass = float(config["constants"]["gm_sun"]) / grav_const

    # Compute the SOI of planet Earth
    soi_res_earth = SolarY.general.dynamics.properties.sphere_of_influence(
        sem_maj_axis=sem_maj_axis_earth, minor_mass=earth_mass, major_mass=sun_mass
    )

    # Assertion test with the SOI's expectation
    assert pytest.approx(soi_res_earth, abs=1e4) == 925000.0
