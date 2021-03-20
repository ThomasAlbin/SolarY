"""
test_parse.py

Testing suite for SolarY/auxiliary/parse.py

"""
import os

import SolarY


def test_comp_md5():
    """
    Test function to check if the function comp_md5 computes the correct MD5 hash value of a mock
    up file.

    Returns
    -------
    None.

    """

    # Create mockup file
    mockup_file = "mockup.txt"
    open(mockup_file, "wb").close()

    # Compute the MD5 has and compare the result with the expectation
    md5_mockup = SolarY.auxiliary.parse.comp_sha256(mockup_file)
    assert md5_mockup == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    # Remove the mockup file from the system
    os.remove(mockup_file)
