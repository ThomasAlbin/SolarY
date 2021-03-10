"""TBW."""
# flake8: noqa
from ._version import get_versions

try:
    from . import asteroid, auxiliary, general, instruments, neo
except ModuleNotFoundError as exc:
    # this occurs when during `tox -e build`, just ignore it.
    print("Import error in Solary.__init__. Exception:", exc)

__version__ = get_versions()["version"]  # type: ignore
__date__ = get_versions()["date"]  # type: ignore
__project__ = "SolarY"
__author__ = "Dr.-Ing. Thomas Albin"
# __version__ = "deploy"
