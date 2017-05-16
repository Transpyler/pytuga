'''
================
Standard library
================

Transpyler makes all standard python functions. We also provide some additional
functions.

.. automodule:: tugalib.tuga_io
.. automodule:: tugalib.tuga_strings
.. automodule:: tugalib.tuga_math
.. automodule:: tugalib.tuga_std
.. automodule:: tugalib.tuga_draw

'''

from .tuga_io import *
from .tuga_math import *
from .tuga_std import *
from .tuga_strings import *

# Register synonyms
from transpyler import utils

globals().update(utils.collect_synonyms(globals()))
del utils
del synonyms
