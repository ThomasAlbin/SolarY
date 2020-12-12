import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

__project__ = "SolarY"
__author__ = "Dr.-Ing. Thomas Albin"
__version__ = "ON_GIT_RELEASE"

from . import _config

from . import tests

from . import auxiliary
from . import general
from . import asteroid
from . import neo
