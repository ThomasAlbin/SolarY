"""
test_vec.py

Testing suite for solary/general/vec.py

"""

# Import standard libraries
import math

# Import installed libraries
import pytest

# Import solary
import solary


def test_norm():
    """
    Testing the vector norm computation.

    Returns
    -------
    None.

    """

    # Compute the length of a unit vector
    vec_norm_res1 = solary.general.vec.norm(vector=[1.0, 0.0])
    assert vec_norm_res1 == 1.0

    # Compute the length of a 45 degrees vector
    vec_norm_res2 = solary.general.vec.norm(vector=[1.0, 1.0])
    assert vec_norm_res2 == math.sqrt(2)

    # Example #3
    vec_norm_res3 = solary.general.vec.norm(vector=[5.0, 4.0])
    assert vec_norm_res3 == math.sqrt(41)

    # Example #4
    vec_norm_res4 = solary.general.vec.norm(vector=[1.0, 1.0, 1.0])
    assert vec_norm_res4 == math.sqrt(3)

    # Example #5
    vec_norm_res5 = solary.general.vec.norm(vector=[2.0, 4.0, -5.0, 6.0])
    assert vec_norm_res5 == 9.0


def test_unify():
    """
    Testing the function that normalises a vector.

    Returns
    -------
    None.

    """

    # A unified unit vector must correspond to the input
    unit_vec1 = solary.general.vec.unify(vector=[1.0, 0.0, 0.0])
    assert unit_vec1 == [1.0, 0.0, 0.0]

    # Example #2
    unit_vec2 = solary.general.vec.unify(vector=[5.0, 0.0, 0.0])
    assert unit_vec2 == [1.0, 0.0, 0.0]

    # Example #3
    unit_vec3 = solary.general.vec.unify(vector=[5.0, 5.0, 5.0])
    assert pytest.approx(unit_vec3) == [1.0 / math.sqrt(3), 1.0 / math.sqrt(3), 1.0 / math.sqrt(3)]


def test_dot_prod():
    """
    Testing suite for the computation of the dot product.

    Returns
    -------
    None.

    """

    # Example #1
    dot_res1 = solary.general.vec.dot_prod(vector1=[1.0, 2.0, 3.0], \
                                           vector2=[-2.0, 5.0, 8.0])
    assert dot_res1 == 32.0

    # Example #2
    dot_res2 = solary.general.vec.dot_prod(vector1=[-10.0, 20.0], \
                                           vector2=[-1.0, 0.0])
    assert dot_res2 == 10.0

    # Example #3
    dot_res3 = solary.general.vec.dot_prod(vector1=[23.0, 10.0], \
                                           vector2=[2.0, 0.01])
    assert dot_res3 == 46.1


def test_phase_angle():
    """
    Testing the computation of the phase angle between two vectors.

    Returns
    -------
    None.

    """

    # Example #1: Phase angle of 90 degrees
    angle_res1 = solary.general.vec.phase_angle(vector1=[1.0, 0.0], \
                                                vector2=[0.0, 1.0])
    assert angle_res1 == math.pi / 2.0

    # Example #2: Phase angle of 180 degrees
    angle_res2 = solary.general.vec.phase_angle(vector1=[1.0, 0.0], \
                                                vector2=[-1.0, 0.0])
    assert angle_res2 == math.pi

    # Example #3: Phase angle of 0 degrees
    angle_res3 = solary.general.vec.phase_angle(vector1=[1.0, 0.0], \
                                                vector2=[1.0, 0.0])
    assert angle_res3 == 0.0


def test_substract():
    """
    Testing the substraction of two vectors.

    Returns
    -------
    None.

    """

    # Example #1
    vec_diff1 = solary.general.vec.substract(vector1=[4.0, 7.0], \
                                             vector2=[5.0, 1.0])
    assert vec_diff1 == [-1.0, 6.0]

    # Example #2
    vec_diff2 = solary.general.vec.substract(vector1=[-4.0, -4.0], \
                                             vector2=[-5.0, 9.0])
    assert vec_diff2 == [1.0, -13.0]


def test_inverse():
    """
    Testing the vector inversion.

    Returns
    -------
    None.

    """

    # Example #1
    inverse_vec1 = solary.general.vec.inverse(vector=[1.0, 5.0])
    assert inverse_vec1 == [-1.0, -5.0]

    # Example #2
    inverse_vec2 = solary.general.vec.inverse(vector=[-5.1, -100.0, 0.0])
    assert inverse_vec2 == [5.1, 100.0, 0.0]
