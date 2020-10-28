"""
vec.py

Auxiliary functions for vector computations.

"""

# Import standard libraries
import math


def norm(vector):
    """
    This function computes the norm of a given vector. The current version computes only the
    Euclidean Norm, respectivels the p2 norm.

    Parameters
    ----------
    vector : list
        Input vector of any dimensionality.

    Returns
    -------
    norm_res : float
        Norm of the input vector.

    Examples
    --------
    >>> import solary
    >>> vec_norm = solary.general.vec.norm(vector=[3.0, 5.0, -5.9])
    >>> vec_norm
    8.295179322956196

    """

    # Compute the norm by summing all squared elements
    norm_res = math.sqrt(sum(abs(elem)**2.0 for elem in vector))

    return norm_res


def unify(vector):
    """
    This function normalises the input vector. So, the elements of the vector are divided by the
    norm of the vector. The result is a unit vector with the length 1.

    Parameters
    ----------
    vector : list
        Input vector of any dimensionality.

    Returns
    -------
    unit_vector : list
        Unified / Normalised vector.

    Examples
    --------
    >>> import solary
    >>> unit_vec = solary.general.vec.unify(vector=[1.0, 5.0, 10.0])
    >>> unit_vec
    [0.0890870806374748, 0.44543540318737396, 0.8908708063747479]

    Now check the norm of the resulting vector

    >>> vec_norm = solary.general.vec.norm(vector=unit_vec)
    >>> vec_norm
    1.0

    """

    # Compute the norm of the input vector
    vector_norm = norm(vector)

    # Iterate through all input vector elements and normalise them
    unit_vector = [vector_elem / vector_norm for vector_elem in vector]

    return unit_vector


def dot_prod(vector1, vector2):
    """
    This function computes the dot product between two given vectors.

    Parameters
    ----------
    vector1 : list
        Input vector #1 of any dimensionality.
    vector2 : list
        Input vector #2 with the same dimensionality as vector1.

    Returns
    -------
    dotp_res : float
        Dot product of both vectors.

    Examples
    --------
    >>> import solary
    >>> dot_product_res = solary.general.vec.dot_prod(vector1=[1.5, -4.0, 8.0], \
                                                      vector2=[-5.0, -4.20, 0.0])

    >>> dot_product_res
    9.3

    """

    # Compute dot product
    dotp_res = sum(v1_i * v2_i for v1_i, v2_i in zip(vector1, vector2))

    return dotp_res


def phase_angle(vector1, vector2):
    """
    This function compute the phase angle between two vectors. The phase angle is the enclosed
    angle between the vectors at their corresponding point of origin.

    The output is given in radians and ranges from 0 to pi.

    Parameters
    ----------
    vector1 : list
        Input vector #1 of any dimensionality.
    vector2 : list
        Input vector #2 with the same dimensionality as vector1.

    Returns
    -------
    angle_rad : float
        Phase angle in radians between vector1 and vector2.

    Examples
    --------
    >>> import math
    >>> import solary
    >>> ph_angle_rad = solary.general.vec.phase_angle(vector1=[1.0, 0.0], \
                                                      vector2=[1.0, 1.0])
    >>> ph_angle_deg = math.degrees(ph_angle_rad)
    >>> ph_angle_deg
    45.0

    """

    # Compute the phase angle by considering the rearranged, known geometric definition of the dot
    # product
    angle_rad = math.acos(dot_prod(vector1, vector2) \
                          / (norm(vector1) * norm(vector2)))

    return angle_rad


def substract(vector1, vector2):
    """
    This function substracts the vector elements of one list with the elements of another list.
    Alternatively, one can use the Numpy library and Numpy arrays without using this function at
    all.

    Parameters
    ----------
    vector1 : list
        Input vector #1 of any dimensionality.
    vector2 : list
        Input vector #2 with the same dimensionality as vector1.

    Returns
    -------
    diff_vector : list
        Difference vector with the same dimensionality as vector1.

    Examples
    --------
    >>> import solary
    >>> vector_diff = solary.general.vec.substract(vector1=[1.0, 4.0, 2.0], \
                                                   vector2=[-8.0, 0.0, 1.0])
    >>> vector_diff
    [9.0, 4.0, 1.0]

    """

    # Set an empty list for the vector difference / substraction
    diff_vector = []

    # Zip both input vector
    zipped_vector = zip(vector1, vector2)

    # Iterate through all elements and compute the substraction
    for vector1_i, vector2_i in zipped_vector:
        diff_vector.append(vector1_i - vector2_i)

    return diff_vector


def inverse(vector):
    """
    Inverse the vector's elements. Alternatively, apply -1 on a Numpy array.

    Parameters
    ----------
    vector : list
        Input vector of any dimensionality.

    Returns
    -------
    inv_vector : TYPE
        Inverse output vector with the same dimensionality as vector.

    Examples
    --------
    >>> import solary
    >>> inverse_vector = solary.general.vec.inverse(vector=[1.0, 2.0, -3.0])
    >>> inverse_vector
    [-1.0, -2.0, 3.0]

    """

    # Inverse the vector element entries by multiplying -1.0 to each element
    inv_vector = [-1.0 * vector_elem for vector_elem in vector]

    return inv_vector
