"""Auxiliary functions for file and path parsing."""
import hashlib
import os
import pathlib
import typing as t

from .config import root_dir


def comp_sha256(file_name: t.Union[str, pathlib.Path]) -> str:
    """
    Compute the SHA256 hash of a file.

    Parameters
    ----------
    file_name : str
        Absolute or relative pathname of the file that shall be parsed.

    Returns
    -------
    sha256_res : str
        Resulting SHA256 hash.
    """
    # Set the MD5 hashing
    hash_sha256 = hashlib.sha256()

    # Open the file in binary mode (read-only) and parse it in 65,536 byte chunks (in case of
    # large files, the loading will not exceed the usable RAM)
    with pathlib.Path(file_name).open(mode="rb") as f_temp:
        for _seq in iter(lambda: f_temp.read(65536), b""):
            hash_sha256.update(_seq)

    # Digest the MD5 result
    sha256_res = hash_sha256.hexdigest()

    return sha256_res


def setnget_file_path(dl_path: str, filename: str) -> str:
    """
    Compute the path of a file, depending on its download path.

    The standard download path is:
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
    home_dir = os.path.expanduser("~")

    # Join the home directory path with the download path
    compl_dl_path = os.path.join(home_dir, dl_path)

    # Create the download path, if it does not exists already (recursively)
    pathlib.Path(compl_dl_path).mkdir(parents=True, exist_ok=True)

    # Join the home dir. + download dir. with the filename
    file_path = os.path.join(compl_dl_path, filename)

    return file_path


def get_test_file_path(file_path: str) -> str:
    """
    Compute the absolute path to a file within the testing suite.

    Parameters
    ----------
    file_path : str
        Relative filepath of the test file w.r.t. the root directory.

    Returns
    -------
    compl_test_file_path : str
        Absolute filepath to the testing file.
    """
    # Join the root directory of SolarY with the given filepath.
    # root_dir = os.path.dirname(importlib.import_module("SolarY").__file__)
    compl_test_file_path = os.path.join(root_dir, file_path)

    return compl_test_file_path
