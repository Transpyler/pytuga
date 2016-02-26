"""
Dirty c-level hacks inspired by the forbiddenfruit module.
"""

import os
import ctypes
from .util import unidecode, accented_keywords, synonyms, collect_synonyms


__all__ = ['Lista', 'Tupla', 'Conjunto', 'Dicionário', 'Texto']
#
# These classes are mixed with regular builtins using the forbiddenfruit
# package
#
class Lista(list):
    """Uma lista representa uma sequência de objetos.

    Pode ser incializada com a sintaxe::

    >>> L = [1, 2, 3, 4]
    """

    @synonyms('acrescente')
    def acrescentar(self, elemento):
        """Acrescenta um elemento no final da lista."""

        self.append(elemento)

    @synonyms('limpe')
    def limpar(self):
        """Remove todos os elementos, ficando vazio."""

        self.clear()

    def cópia(self):
        """Retorna uma cópia da lista."""

        return self.copy()

    @synonyms('conte')
    def contar(self, valor):
        """Retorna o número de ocorrências do valor dado."""

        return self.count(valor)

    @synonyms('estenda')
    def estender(self, seq):
        """Adiciona todos os elementos da sequência dada no fim da lista."""

        self.extend(seq)

    def índice(self, valor, *args):
        """Retorna o índice da primeira ocorrência do valor fornecido."""

        return self.index(valor, *args)

    def índice_em_intervalo(self, valor, i, j):
        """Retorna o índice da primeira ocorrência do valor fornecido no
        intervalo entre i e j."""

        return self.index(valor, i, j)

    @accented_keywords
    @synonyms('insira')
    def inserir(self, índice, valor):
        """Insere o elemento dado na posição dada pelo índice."""

        self.insert(índice, valor)

    @synonyms('remova')
    def remover(self, valor):
        """Remove primeira ocorrência de um elemento com o valor fornecido."""

        self.remove(valor)

    @synonyms('inverta')
    def inverter(self):
        """Reordena a lista na ordem inversa."""

        self.reverse()

    @synonyms('ordene')
    def ordenar(self, **kwds):
        """Ordena a lista."""

        self.sort(**kwds)

    @accented_keywords
    @synonyms('ordene_por')
    def ordenar_por(self, função, invertido=False):
        """Ordena a lista a partir segundo o resultado da aplicação da função
        dada em cada elemento."""

        self.sort(key=função, reverse=invertido)

    @synonyms('retire', 'retirar_último', 'retire_último')
    def retirar(self, *args):
        """Remove o último elemento da lista e o retorna."""

        return self.pop(*args)

    @accented_keywords
    @synonyms('retire_de')
    def retirar_de(self, índice):
        """Remove o elemento no índice dado e o retorna."""

        return self.pop(índice)


class Tupla(tuple):
    """Uma tupla funciona como uma lista imutável de elementos.

    Tuplas podem ser chaves de dicionários, enquanto listas não.

    Pode ser incializada com a sintaxe::

    >>> pto = (1, 2, 3)
    """

    contar = Lista.contar
    índice = Lista.índice
    índice_em_intervalo = Lista.índice_em_intervalo


class Conjunto(set):
    """Um conjunto guarda apeanas uma cópia de cada elemento distinto fornecido.
    Conjuntos não possuem ordenamento defindo e são inicializados com a
    sintaxe::

    >>> C = {1, 1, 2, 3}  # equivalente à {1, 2, 3}
    """

    # Single element operations
    adicionar = adicione = set.add
    retirar = Lista.retirar
    remover = Lista.remover
    limpar = Lista.limpar
    cópia = Lista.cópia
    descartar = descarte = set.discard

    # Set properties
    é_disjunto = set.isdisjoint
    é_subconjunto = set.issubset
    é_superconjunto = set.issuperset

    # Set operations
    diferença = set.difference
    intersecção = interseção = set.intersection
    diferença_simétrica = set.symmetric_difference
    união = set.union

    # Set update
    atualizar = atualize = set.update
    atualizar_com_diferença = atualize_com_diferença = set.difference_update
    atualizar_com_diferença_simétrica = atualize_com_diferença_simétrica = \
        set.symmetric_difference_update
    atualizar_com_intersecção = atualizar_com_interseção = \
        atualize_com_intersecção = atualize_com_interseção = \
        set.intersection_update


class Dicionário(dict):
    """Dicionário representa um mapa entre um conjunto de chaves e seus
    respectivos valores.

    Pode ser incializado com a sintaxe::

    >>> D = {"um": 1, "dois": 2, "três": 3}
    """

    limpar = Lista.limpar
    cópia = Lista.copy

    # = dict.fromkeys
    obter = obtenha = dict.get

    # Iterators
    itens = dict.items
    chaves = dict.keys
    valores = dict.values

    padrão = dict.setdefault
    atualizar = atualize = dict.update
    retirar = retire = dict.pop
    retirar_item = retire_item = dict.popitem


class Texto(str):
    """Representa uma sequência de letras em um texto.

    Envolvemos o conteúdo do texto em aspas simples ou duplas::

    >>> texto1 = "Olá, mundo!"
    >>> texto2 = 'Aspas simples também funcionam ;-)'
    """

    # Case control
    capitalizado = str.capitalize
    minúsculas = str.lower
    maiúsculas = str.upper
    normalizado = str.casefold
    caso_trocado = str.swapcase
    título = str.title

    # Aligment
    centralizado = str.center
    justificado_à_esquerda = str.ljust
    justificado_à_direita = str.rjust

    # Queries
    é_alfanumérico = str.isalnum
    é_alfabético = str.isalpha
    é_decimal = str.isdecimal
    é_digito = str.isdigit
    é_numérico = str.isnumeric
    é_identificador = str.isidentifier
    é_minúscula = str.islower
    é_maiúscula = str.isupper
    é_título = str.istitle
    é_imprimível = str.isprintable
    é_espaço = str.isspace

    # TODO: other dict methods
    '''
    = str.count
    = str.encode
    = str.endswith
    = str.expandtabs
    = str.find
    = str.format
    = str.format_map
    = str.index
    = str.join
    = str.lstrip
    = str.maketrans
    = str.partition
    = str.replace
    = str.rfind
    = str.rindex
    = str.rpartition
    = str.rsplit
    = str.rstrip
    = str.split
    = str.splitlines
    = str.startswith
    = str.strip
    = str.translate
    = str.zfill
    '''

#
# In the nomenclature of the forbiddenfruit module, inserting a new method to
# a builtin type is called "cursing". We shall do it a lot in order to provide
# translations.
#
CURSES = {
    list: Lista,
    tuple: Tupla,
    set: Conjunto,
    dict: Dicionário,
    str: Texto,
}

_cpython = ctypes.pythonapi


class SlotsProxy(ctypes.Structure):
    _fields_ = [
        ('ob_refcnt', ctypes.c_ssize_t),
        ('ob_type', ctypes.py_object),
        ('dict', ctypes.py_object),
    ]


def _curse(cls, attr, value):
    target = cls.__dict__
    proxy_dict = SlotsProxy.from_address(id(target))
    proxy_dict.dict[attr] = value


def _apply_curse(tt, curse):
    """Monkey patch the builtin type tt to have all methods of curse. Name and
     docstring are also updated."""

    namespace = {k: v for (k, v) in vars(curse).items() if not k[0] == '_'}
    functions = collect_synonyms(namespace)
    for name, func in functions.items():
        if hasattr(tt, name):
            tname = tt.__name__
            raise ValueError('%s already has a %s() method' % (tname, name))
        _curse(tt, name, func)

    # Apply docstring (not working)
    _curse(tt, '__doc__', curse.__doc__)


def _apply_all_curses():
    """Apply all curses defined by special classes in this module."""

    for tt, curse in CURSES.items():
        _apply_curse(tt, curse)


class _object:
    """Generic type we use to inspect the location of the generic C-level
     repr and str functions.

     All methods supported must provide a placeholder implementation here."""

    __repr__ = __str__ = lambda self: ''


def _repr_offset():
    """How many bytes after id(type) can we find the tp_repr pointer?"""

    return 11 * ctypes.sizeof(ctypes.c_ssize_t)


def _str_offset():
    """How many bytes after id(type) can we find the tp_str pointer?"""

    # str is just 6 places after repr in the type specification
    return _repr_offset() + 6 * ctypes.sizeof(ctypes.c_ssize_t)


def _assure_generic_c_level_function(tt, offset):
    """Makes sure that the given type tt uses the generic c-level function
    for some of the magic methods such as repr(), str(), etc."""

    ref_from_address = ctypes.c_ssize_t.from_address
    tp_func_object = ref_from_address(id(_object) + offset)
    tp_func_cursed = ref_from_address(id(tt) + offset)
    tp_func_cursed.value = tp_func_object.value


def _change_bool_repr():
    """Change repr of True to "verdadeiro" and False to "falso"."""

    def __repr__(self):
        if self:
            return 'Verdadeiro'
        else:
            return 'Falso'

    _curse(bool, '__repr__', __repr__)
    _curse(bool, '__str__', __repr__)
    _assure_generic_c_level_function(bool, _str_offset())
    _assure_generic_c_level_function(bool, _repr_offset())


def _change_none_repr():
    """Change repr of None to "nulo"."""

    def __repr__():
        return 'Nulo'

    _curse(type(None), '__repr__', __repr__)
    _curse(type(None), '__str__', __repr__)
    _assure_generic_c_level_function(type(None), _str_offset())
    _assure_generic_c_level_function(type(None), _repr_offset())


# Apply curses
if os.environ.get('FORBIDDEN_PYTUGA', 'true') == 'true':
    print('''
======================
Aviso aos beta-testers
======================

Esta versão está testando um hack no interpretador do Python que permite
modificar a representação dos tipos base como True, False e None. Se o
interpretador terminar com segfault ou apresentar algum tipo de comportamento
errático reinicie com a variável de ambiente FORBIDDEN_PYTUGA igual à "false" e
envie um relatório de erros com a sua plataforma e sistema operacional.
''')
    _apply_all_curses()
    _change_bool_repr()
    _change_none_repr()