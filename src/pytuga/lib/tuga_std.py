"""
Outras funções
==============

Outras funções que não se encaixam em nenhuma categoria específica.
"""
import time as _time

from transpyler.utils import synonyms, normalize_accented_keywords


#
# Time control
#
@synonyms('durma')
def dormir(intervalo):
    """
    Permanece sem fazer nada o intervalo de tempo fornecido (em segundos).
    """

    _time.sleep(intervalo)


@synonyms('saia')
def sair(código_erro=0):
    """
    Termina a execução do programa fornecendo um código de erro ou código
    de saída.

    Um ``código_erro=0`` sinaliza que o programa terminou com sucesso. Qualquer
    outro número ou um texto representa falha.
    """

    raise SystemExit(código_erro)


#
# Conversions/representations of numerical types
#
def real(x):
    """
    Converte um texto ou número a um número de ponto flutuante.

    Examples:
        >>> real(5)
        5.0
        >>> real(673.23)
        673.23
        >>> real("673.23")
        673.23
    """

    return float(x)


def inteiro(x):
    """
    Converte um número ou texto num inteiro, ou retorna 0 se nenhum argumento
    for fornecido.

    Examples:
        >>> int(4.3)
        4
        >>> int(44.6E-1)
        4
        >>> int()
        0
    """

    return int(x)


def booleano(x):
    """
    Retorna verdadeiro quando o argumento x é verdadeiro, falso em caso
    contrário.

    Os booleanos podem ser usados como inteiros, sendo que falso equivale a 0 e
    verdadeiro equivale a 1.

    Examples:
        >>> booleano(0)
        Falso
        >>> booleano(1)
        Verdadeiro
    """

    return bool(x)


def binário(x):
    """
    Retorna a representação binária de um [inteiro/número inteiro].

    Examples:
        >>> bin(2796202)
        '0b1010101010101010101010'
    """

    return bin(x)


def octal(x):
    """
    Retorna a representação octal de um inteiro.

    Examples:
        >>> octal(22052015)
        '0o124076257'
    """
    return oct(x)


def hexadecimal(x):
    """
    Retorna a representação hexadecimal de um inteiro.

    Examples:
        >>> hex(6745)
        '0x1a59'
    """
    return hex(x)


def caractere(x):
    """
    Retorna um texto Unicode associado a um ordinal (Unicode é um padrão de
    representãção de qualquer caractere de um sistema de escrita).

    Examples:
        >>> caractere(227)
        'ã'
        >>> caractere(231)
        'ç'
        >>> caractere(224)
        'à'
    """

    return chr(x)


#
# Sequence operations
#
def tamanho(x):
    """
    Retorna o número de itens de uma sequência ou coleção.

    Examples:
        >>> texto = "programando em python"
        >>> tamanho(texto)
        21
    """
    return len(x)


@synonyms('enumere')
def enumerar(x):
    """
    Retorna uma enumeração.

    Examples:
        >>> música = ['uni', 'duni', 'te']
        >>> listar(enumerar(música))
        [(0, 'uni'), (1, 'duni'), (2, 'te')]
    """

    return enumerate(x)


def dicionário(dados, **kwds):
    """
    Retorna um dicionário a partir da sequẽncia de elementos (chave, valor).

    Examples:
        >>> dicionário([(0, 'zero'), (1, 'um'), (2, 'dois')])
        {0: 'zero', 1: 'um', 2: 'dois'}
    """

    return dict(dados, **kwds)


def tupla(x):
    """
    Retorna uma tupla com todos os elementos da sequência fornecida.
    Uma tupla se assemelha com uma lista, mas não pode ser modificada após
    criada.

    Examples:
        >>> tupla([1, 2, 3])
        (1, 2, 3)
    """
    return tuple(x)


def lista(seq=None):
    """
    Cria uma lista a partir da sequência fornecida.

    Se nenhuma sequência for fornecida, retorna uma lista vazia.
    """

    if seq is None:
        return []
    return list(seq)


@synonyms('liste')
def listar(seq):
    """
    Retorna uma lista com todos os elementos da sequência fornecida.

    Examples:
        >>> listar('olá')
        ['o', 'l', 'á']
    """
    return list(seq)


@synonyms('liste_invertido')
def listar_invertido(seq):
    """
    Lista os elementos da sequência fornecida na ordem inversa.

    Examples:
        >>> música = ['uni', 'duni', 'te']
        >>> listar_invertido(música)
        ['te', 'duni', 'uni']
    """

    return list(reversed(seq))


def ordenado(seq, chave=None):
    """
    Retorna uma cópia da sequência fornecida com os elementos ordenados.

    Examples:
        >>> sorted([5, 2, 3, 1, 4])
        [1, 2, 3, 4, 5]
    """
    return sorted(seq, key=chave)


@normalize_accented_keywords
def texto(obj, codificacao=None):
    """
    Cria um novo texto a partir do objeto fornecido.

    Examples:
        >>> texto(42)
        "42"
    """
    if codificacao is None:
        return str(obj)
    return str(obj, encoding=codificacao)


#
# Other functions
#
def tipo(x):
    """
    Retorna o tipo do objeto.

    Examples:
        >>> tipo(2) == inteiro
        Verdadeiro
    """

    # Disabled type(name, bases, namespace) since we don't expect begginers
    # messing up with metaclasses ;-)
    return type(x)


def ajuda(*args):
    """
    Fornece ajuda sobre módulos, palavras chaves ou tôpicos do Pytuguês.

    Pode ser chamada sem argumentos como `ajuda()` para uma ajuda geral sobre
    como utilizar o Pytuguês ou pode ser chamada com um argumento (como em
    `ajuda(binário)` para obter ajuda sobre um tópico específico.
    """

    # TODO: criar função ajuda interativa em português
    if not args:
        return help()
    else:
        return help(*args)


#
# Singleton objects
#
verdadeiro = Verdadeiro = True
falso = Falso = False
nulo = Nulo = None

#
# Type alias
#
Lista = list
Tupla = tuple
Dicionário = dict
Conjunto = set
ConjuntoImutável = frozenset
Texto = Cadeia = str
Inteiro = int
Fracionário = float
Complexo = complex

#
# Pending functions. Will we have support?
#
# format = format
# ord = ord
# bytes = bytes
