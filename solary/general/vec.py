"""
vec.py

Auxiliary function for vector computations

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

    """

    # Compute the phase angle by considering the rearranged, known geometric definition of the dot
    # product
    angle_rad = math.acos(dot_prod(vector1, vector2) \
                          / (norm(vector1) * norm(vector2)))

    return angle_rad

def substract(vector1, vector2):
    
    # Set an empty list for the vector difference / substraction
    diff_vector = []

    # Zip both input vector
    zipped_vector = zip(vector1, vector2)

    # Iterate through all elements and compute the substraction
    for vector1_i, vector2_i in zipped_vector:
        diff_vector.append(vector1_i - vector2_i)
    
    return diff_vector

def inverse(vector):

    # Inverse the vector element entries by multiplying -1.0 to each element
    inv_vector = [-1.0 * vector_elem for vector_elem in vector]
    
    return inv_vector
