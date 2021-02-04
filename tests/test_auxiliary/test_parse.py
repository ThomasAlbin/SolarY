"""
test_parse.py

Testing suite for solary/auxiliary/parse.py

"""

# Import standard libraries
import os

# Import solary
import solary


def test_comp_md5():
    """
    Test function to check if the function comp_md5 computes the correct MD5 hash value of a mock
    up file.

    Returns
    -------
    None.

    """

    # Create mockup file
    mockup_file = 'mockup.txt'
    open(mockup_file, 'wb').close()

    # Compute the MD5 has and compare the result with the expectation
    md5_mockup = solary.auxiliary.parse.comp_md5(mockup_file)
    assert md5_mockup == 'd41d8cd98f00b204e9800998ecf8427e'

    # Remove the mockup file from the system
    os.remove(mockup_file)
