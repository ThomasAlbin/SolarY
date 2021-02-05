"""
test_download.py

Testing suite for solary/auxiliary/download.py

"""

# Import solary
import solary

import logging


def test_spice_generic_kernels():
    
    solary.auxiliary.download.spice_generic_kernels()