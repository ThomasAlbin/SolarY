"""
test_photometry.py

Testing suite for solary/general/photometry.py

"""

# Import standard libraries
import math

# Import installed libraries
import pytest

# Import solary
import solary


def test_appmag2irr():
    """
    Testing the function appmag2irr that converts the apparent magnitude to an irradiance in W/m^2

    Returns
    -------
    None.

    """

    # Read the constants file and get the bolometric zero value
    config = solary.auxiliary.config.get_constants()
    appmag_irr_i0 = float(config['photometry']['appmag_irr_i0'])

    # The apparent magnitude of 0 mag must correspond to the bolometric 0 value
    irradiance1 = solary.general.photometry.appmag2irr(app_mag=0)
    assert pytest.approx(irradiance1) == appmag_irr_i0

    # -5 mag must be 100 brighter than the bolometric zero value
    irradiance2 = solary.general.photometry.appmag2irr(app_mag=-5)
    assert pytest.approx(irradiance2) == appmag_irr_i0 * 100.0

    # Another example
    irradiance3 = solary.general.photometry.appmag2irr(app_mag=1)
    assert pytest.approx(irradiance3) == 1.0024422165005002e-08


def test_phase_func():
    """
    This function tests the phase function that is needed for the apparent magnitude computation of
    minor bodies

    Returns
    -------
    None.

    """

    # Example 1
    phi1_res1 = solary.general.photometry.phase_func(index=1, phase_angle=0.0)
    assert phi1_res1 == 1.0

    # Example 2
    phi2_res1 = solary.general.photometry.phase_func(index=1, phase_angle=0.0)
    assert phi2_res1 == 1.0

    # Example 3
    phi1_res2 = solary.general.photometry.phase_func(index=1, phase_angle=math.pi/2.0)
    assert phi1_res2 == 0.03579310506765532

    # Example 4
    phi2_res2 = solary.general.photometry.phase_func(index=2, phase_angle=math.pi/2.0)
    assert phi2_res2 == 0.15412366181513143


def test_reduc_mag():
    """
    Testing the function that computed the reduced magnitude.

    Returns
    -------
    None.

    """

    # An absolute magnitude of 0 and a phase angle of 0 degrees must correspond to a reduced
    # magnitude of 0
    red_mag1 = solary.general.photometry.reduc_mag(abs_mag=0, slope_g=0.15, phase_angle=0.0)
    assert red_mag1 == 0.0

    # Second artifically set and computed example
    red_mag2 = solary.general.photometry.reduc_mag(abs_mag=0, slope_g=0.15, phase_angle=math.pi/2.0)
    assert red_mag2 == 3.178249562605391


def test_hg_app_mag():
    """
    Testing the computation of the apparent magnitude (H-G system).

    Returns
    -------
    None.

    """

    # Set sample vectors (example: first vector is an asteroid at 2 AU, second vector is planet
    # Earth at 1 AU)
    vec_obj1 = [2.0, 0.0, 0.0]
    vec_obs1 = [1.0, 0.0, 0.0]

    # Compute the vector object -> observer
    vec_obj2obs1 = solary.general.vec.substract(vector1=vec_obs1, vector2=vec_obj1)

    # Compute the vector object -> illumination source (by inversing the object vector to
    # [-2.0, 0.0, 0.0])
    vec_obj2ill1 = solary.general.vec.inverse(vector=vec_obj1)

    # Compute the apparent magnitude for an object with an absolute magnitude of 0.0 mag and a
    # slope parameter of 0.15 (default value for asteroids).
    app_mag1 = solary.general.photometry.hg_app_mag(abs_mag=0.0, \
                                                    slope_g=0.15, \
                                                    vec_obj2obs=vec_obj2obs1, \
                                                    vec_obj2ill=vec_obj2ill1)
    assert app_mag1 == 1.505149978319906


    # Second example with simplified values for (1) Ceres (at opposition w.r.t. Earth)
    vec_obj2 = [3.0, 0.0, 0.0]
    vec_obs2 = [1.0, 0.0, 0.0]

    vec_obj2obs2 = solary.general.vec.substract(vector1=vec_obs2, \
                                                vector2=vec_obj2)
    vec_obj2ill2 = solary.general.vec.inverse(vector=vec_obj2)

    app_mag2 = solary.general.photometry.hg_app_mag(abs_mag=3.4, \
                                                    slope_g=0.12, \
                                                    vec_obj2obs=vec_obj2obs2, \
                                                    vec_obj2ill=vec_obj2ill2)

    # Ceres has a brightness of around 7 mag at opposition
    assert app_mag2 == 7.290756251918218

    # Third example with the same values but a larger phase angle
    vec_obj3 = [0.0, 3.0, 0.0]
    vec_obs3 = [1.0, 0.0, 0.0]

    vec_obj2obs3 = solary.general.vec.substract(vector1=vec_obs3, \
                                                vector2=vec_obj3)
    vec_obj2ill3 = solary.general.vec.inverse(vector=vec_obj3)

    app_mag3 = solary.general.photometry.hg_app_mag(abs_mag=3.4, \
                                                    slope_g=0.12, \
                                                    vec_obj2obs=vec_obj2obs3, \
                                                    vec_obj2ill=vec_obj2ill3)

    # A larger phase angle should lead to a smaller brightness (larger apparent magnitude);
    # compared to the opposition result
    assert app_mag3 > app_mag2
