"""
test_download.py

Testing suite for SolarY/auxiliary/download.py

"""
import SolarY


def test_spice_generic_kernels():
    """
    Test function for the download function spice_generic_kernels.

    Returns
    -------
    None.

    """

    # Load the generic kernels config file
    paths_config = SolarY.auxiliary.config.get_spice_kernels(ktype="generic")

    # Create a dictionary that will contain the filepath and the corresponding MD5 has values for
    # each SPICE kernel (expectation)
    exp_kernel_dict = {}

    # Iterate trough the config file. Each section is an individual kernel
    for kernel in paths_config.sections():

        # Create the absolute filepath for of each kernel
        _download_filename = SolarY.auxiliary.parse.setnget_file_path(
            paths_config[kernel]["dir"], paths_config[kernel]["file"]
        )

        # Assign the filepath as a dict key and set the SHA256 hash as the corresponding value
        exp_kernel_dict[_download_filename] = paths_config[kernel]["sha256"]

    # Execute the SPICE download function. The resulting dictionary contains the resulting
    # filepaths and SHA256 hashes that shall ...
    res_dl_kernel_dict = SolarY.auxiliary.download.spice_generic_kernels()

    # ... correspond with the expectations
    assert res_dl_kernel_dict == exp_kernel_dict
