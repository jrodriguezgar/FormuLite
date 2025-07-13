"""
Formulite - A Python library for high-level functions similar to Excel formulas.

This library provides a collection of functions that mimic Excel formula functionality
while following Python best practices and providing additional features.

Modules:
    fxDate: Date and time manipulation functions
    fxNumeric: Numeric operations and calculations
    fxPython: Python-specific utilities and helper functions

Version: 0.0.1
Author: DatamanEdge
License: Proprietary
"""

__version__ = "0.0.1"
__author__ = "DatamanEdge"

from .fxDate.date_convertions import *
from .fxDate.date_excel import *
from .fxDate.date_operations import *
from .fxDate.date_sys import *

from .fxNumeric.numeric_convertions import *
from .fxNumeric.numeric_operations import *

from .fxPython.py_classes import *
from .fxPython.py_convertions import *
from .fxPython.py_operations import *
from .fxPython.py_tools import *

from .fxString.string_convertions import *
from .fxString.string_evaluations import *
from .fxString.string_format import *
from .fxString.string_grammar import *
from .fxString.string_operations import *
from .fxString.string_similarity import *
from .fxString.string_spanish import *
