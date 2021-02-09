"""
download.py

This sub-module contains auxiliary functions to download miscellaneous datasets.

"""

# Import standard libraries
import urllib.parse
import urllib.request

# Import solary
from . import config
from . import parse

# Get the file paths
GENERIC_KERNEL_CONFIG = config.get_spice_kernels(ktype='generic')


def spice_generic_kernels():
    """
    Function to download the generic SPICE kernels into the solary data storage directory:
    ~HOME/solary_data/.

    Parameters
    ----------
    None.

    Returns
    -------

    """

    # Set a placeholder list for the filepaths and corresponding / resulting MD5 values
    kernel_hashes = {}

    # Iterate through the SPICE config file. Each section corresponds to an individual SPICE kernel
    for kernel in GENERIC_KERNEL_CONFIG.sections():

        # Set the download filepath
        download_filename = parse.setnget_file_path(GENERIC_KERNEL_CONFIG[kernel]['dir'],
                                                    GENERIC_KERNEL_CONFIG[kernel]['file'])

        # Download the file and store it in the kernels directory
        downl_file_path, _ = urllib.request.urlretrieve(url=GENERIC_KERNEL_CONFIG[kernel]['url'], \
                                                        filename=download_filename)

        # Compute the MD5 hash value
        md5_hash = parse.comp_md5(downl_file_path)

        # Append the filepath and MD5 in the dictionary
        kernel_hashes[download_filename] = md5_hash

    return kernel_hashes
