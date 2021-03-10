"""TBW."""
# flake8: noqa
from . import asteroid, auxiliary, general, instruments, neo
from ._version import get_versions

__version__ = get_versions()["version"]  # type: ignore
__date__ = get_versions()["date"]  # type: ignore
__project__ = "SolarY"
__author__ = "Dr.-Ing. Thomas Albin"
# __version__ = "deploy"
