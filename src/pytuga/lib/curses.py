"""
Dirty c-level hacks inspired by the forbiddenfruit module.
"""

from transpyler import curses
from transpyler.utils import normalize_accented_keywords, synonyms

__all__ = []


#
# These classes are mixed with regular builtins using the same technics as in
# the forbiddenfruit package
#
class Lista(list):
    """
    Uma lista representa uma sequência de objetos.

    Pode ser incializada com a sintaxe:

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

    @normalize_accented_keywords
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

    @normalize_accented_keywords
    @synonyms('ordene_por')
    def ordenar_por(self, função, invertido=False):
        """Ordena a lista a partir segundo o resultado da aplicação da função
        dada em cada elemento."""

        self.sort(key=função, reverse=invertido)

    @synonyms('retire', 'retirar_último', 'retire_último')
    def retirar(self, *args):
        """Remove o último elemento da lista e o retorna."""

        return self.pop(*args)

    @normalize_accented_keywords
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
    """
    Dicionário representa um mapa entre um conjunto de chaves e seus
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
    """
    Representa uma sequência de letras em um texto.

    Envolvemos o conteúdo do texto em aspas simples ou duplas:

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

    # TODO: other str methods?
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


def apply_curses():
    """
    Apply all curses.
    """

    curses.curse_none_repr('Nulo')
    curses.curse_bool_repr('Verdadeiro', 'Falso')
    curses.apply_curses({
        list: Lista,
        tuple: Tupla,
        set: Conjunto,
        dict: Dicionário,
        str: Texto,
    })
