"""
parse.py

Auxiliary functions for file and path parsing

"""

# Import standard libraries
import hashlib
import pathlib
import os


def comp_md5(file_name):
    """
    Compute the MD5 hash of a file.

    Parameters
    ----------
    file_name : str
        Absolute or relative pathname of the file that shall be parsed.

    Returns
    -------
    md5_res : str
        Resulting MD5 hash.

    """

    # Set the MD5 hashing
    hash_md5 = hashlib.md5()

    # Open the file in binary mode (read-only) and parse it in 65,536 byte chunks (in case of
    # large files, the loading will not exceed the usable RAM)
    with open(file_name, 'rb') as f_temp:
        for _seq in iter(lambda: f_temp.read(65536), b''):
            hash_md5.update(_seq)

    # Digest the MD5 result
    md5_res = hash_md5.hexdigest()

    return md5_res


def setnget_file_path(dl_path, filename):
    """
    Compute the path of a file, depending on its download path. The standard download path is:
        ~$HOME/

    Parameters
    ----------
    dl_path : str
        Relative path of the directory where the file is stored (relative to ~$HOME/solary_data/).
    filename : str
        File name.

    Returns
    -------
    file_path : str
        Absolute file name path of the given file name and directory.

    """

    # Get the system's home directory
    home_dir = os.path.expanduser('~')

    # Join the home directory path with the download path
    compl_dl_path = os.path.join(home_dir, dl_path)

    # Create the download path, if it does not exists already (recursively)
    pathlib.Path(compl_dl_path).mkdir(parents=True, exist_ok=True)

    # Join the home dir. + download dir. with the filename
    file_path = os.path.join(compl_dl_path, filename)

    return file_path
