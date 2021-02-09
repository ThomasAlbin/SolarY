"""
test_download.py

Testing suite for solary/auxiliary/download.py

"""

# Import solary
import solary


def test_spice_generic_kernels():
    """
    Test function for the download function spice_generic_kernels.

    Returns
    -------
    None.

    """

    # Load the generic kernels config file
    paths_config = solary.auxiliary.config.get_spice_kernels(ktype='generic')

    # Create a dictionary that will contain the filepath and the corresponding MD5 has values for
    # each SPICE kernel (expectation)
    exp_kernel_dict = {}

    # Iterate trough the config file. Each section is an individual kernel
    for kernel in paths_config.sections():

        # Create the absolute filepath for of each kernel
        _download_filename = solary.auxiliary.parse.setnget_file_path(paths_config[kernel]['dir'],
                                                                      paths_config[kernel]['file'])

        # Assign the filepath as a dict key and set the MD5 hash as the corresponding value
        exp_kernel_dict[_download_filename] = paths_config[kernel]['md5']

    # Execute the SPICE download function. The resulting dictionary contains the resulting
    # filepaths and MD5 hashes that shall ...
    res_dl_kernel_dict = solary.auxiliary.download.spice_generic_kernels()

    # ... correspond with the expectations
    assert res_dl_kernel_dict == exp_kernel_dict
