'''
Funções matemáticas
===================

O pytuga fornece algumas funções matemáticas comuns para a conveniência do
usuário.
'''

import math as _math
pi = _math.pi


def raiz(x):
    '''Retorna a raiz quadrada de x.

    Exemplo
    -------

    >>> raiz(4)
    2.0


    Migração
    --------

    Corresponde à função math.sqrt() no Python
    '''

    return _math.sqrt(x)


def seno(x):
    '''Retorna o seno de x, onde x é medido em radianos.

    Pode ser chamada na forma curta (sen) ou longa (seno).

    Exemplo
    -------

    >>> seno(0)
    0.0
    '''

    return _math.sin(x)
sen = seno


def cosseno(x):
    '''Retorna o cosseno de x, onde x é medido em radianos.

    Pode ser chamada na forma curta (cos) ou longa (cosseno).

    Exemplo
    -------

    >>> cosseno(0)
    1.0
    '''

    return _math.cos(x)
cos = cosseno


def tangente(x):
    '''Retorna a tangente de x, onde x é medido em radianos.

    Pode ser chamada na forma curta (tan) ou longa (tangente).

    Exemplo
    -------

    >>> tangente(0)
    0.0
    '''

    return _math.tan(x)
tan = tangente


def exponencial(x):
    '''Retorna a exponencial de x.

    Pode ser chamada na forma curta (exp) ou longa (exponencial).

    Exemplo
    -------

    >>> exponencial(1)
    2.718281828459045
    >>> exp(1)
    2.718281828459045
    '''

    return _math.exp(x)
exp = exponencial


def logarítimo(x):
    '''Retorna o logarítimo natural de x.

    Pode ser chamada na forma curta (log) ou longa (logarítimo).

    Exemplo
    -------

    >>> logarítimo(1)
    0.0
    >>> log(exp(1))
    1.0
    '''

    return _math.log(x)
log = logarítimo


def log10(x):
    '''Retorna o logarítimo de x na base 10.

    Exemplo
    -------

    >>> log10(10)
    1.0
    '''
    return _math.log10(x)


def módulo(x):
    '''Retorna o módulo de x.

    Exemplo
    -------

    >>> módulo(-1)
    1
    >>> módulo(1)
    1
    '''

    return abs(x)


def arredondar(x):
    '''Arredonda o número x para o inteiro mais pŕoximo.

    Exemplo
    -------

    >>> arredondar(1.6)
    2
    >>> arredondar(1.4)
    1
    '''

    return int(round(x))
arredonde = arredondar


def truncar(x):
    '''Remove a parte decimal do número.

    Exemplo
    -------

    >>> truncar(1.6)
    1
    >>> truncar(1.4)
    1
    '''

    return int(x)
trunque = truncar


def máximo(lista):
    '''Retorna o maior valor da lista dada.

    Exemplo
    -------

    >>> máximo([1, 5, 42, 0])
    42
    '''

    return max(lista)


def mínimo(lista):
    '''Retorna o menor valor da lista dada.

    Exemplo
    -------

    >>> mínimo([1, 5, 42, 0])
    0
    '''

    return min(lista)


def soma(números):
    '''Retorna o resultado da soma da sequência de números dada.

    Exemplo
    -------

    >>> soma([1, 2, 3, 4])
    10
    '''
    return sum(números)


def produto(números):
    '''Retorna o resultado do produto dos números dados.

    Exemplo
    -------

    >>> produto([1, 2, 3, 4, 5])
    120
    '''

    prod = 1
    for x in números:
        prod *= x
    return prod


if __name__ == '__main__':
    import doctest
    doctest.testmod()
