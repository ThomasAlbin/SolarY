"""TBW."""
# flake8: noqa
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

__project__ = "SolarY"
__author__ = "Dr.-Ing. Thomas Albin"
__version__ = "deploy"

from . import _config

# from . import tests

from . import auxiliary
from . import general
from . import asteroid
from . import neo

from . import instruments