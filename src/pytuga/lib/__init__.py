'''
=====================
Biblioteca de funções
=====================

Pytuga consegue carregar qualquer módulo e função disponível no Python. Na
maioria dos casos, utilizaremos as funções definidas especificamente para o
Pytuguês. Boa parte destas funções são simplesmente traduções de funções
correspondentes no Python. Algumas possuem funcionalidade adicional, mas isto
é especificado na documentação.

Aqui mostramos todas as funções disponíveis agrupadas nas categorias abaixo.

.. automodule:: tugalib.tuga_io
.. automodule:: tugalib.tuga_strings
.. automodule:: tugalib.tuga_math
.. automodule:: tugalib.tuga_std
.. automodule:: tugalib.tuga_draw

'''

from .tuga_std import *
from .tuga_strings import *
from .tuga_math import *
from .tuga_io import *

# Register synonyms
from pytuga import utils
utils.register_synonyms(globals())
del utils
del synonyms
