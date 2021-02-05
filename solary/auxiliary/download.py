"""
download.py

This sub-module contains auxiliary functions to download miscellaneous datasets.

"""

# Import standard libraries
import glob
import urllib.parse
import urllib.request
import os

# Import solary
from . import config
from . import parse

# Get the file paths
GENERIC_KERNEL_CONFIG = config.get_spice_kernels(ktype='generic')

def spice_generic_kernels():
    """
    TBW.

    """

    # Set a placeholder list for the resulting MD5 values
    kernel_hashes = {}


    for kernel in GENERIC_KERNEL_CONFIG.sections():
        
        download_filename = \
            parse.setnget_file_path(GENERIC_KERNEL_CONFIG[kernel]['dir'], \
                                                     GENERIC_KERNEL_CONFIG[kernel]['file'])

        # Downlaod the file and store it in the kernels directory
        downl_file_path, _ = urllib.request.urlretrieve(url=GENERIC_KERNEL_CONFIG[kernel]['url'], \
                                                        filename=download_filename)

        # Compute the MD5 hash value
        md5_hash = parse.comp_md5(downl_file_path)

        # Append kernel name and corresponding hash value to the list
        kernel_hashes[download_filename] = md5_hash

    return kernel_hashes
