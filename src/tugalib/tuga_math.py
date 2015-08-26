'''
Funções matemáticas
===================

O pytuga fornece algumas funções matemáticas comuns para a conveniência do
usuário.
'''

import math as _math
import random as _random
from tugalib.util import synonyms
pi = _math.pi
neperiano = _math.exp(1)


#
# Funções elementares e usadas em cálculo científico
#
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


@synonyms('sen')
def seno(x):
    '''Retorna o seno de x, onde x é medido em radianos.

    Pode ser chamada na forma curta (sen) ou longa (seno).

    Exemplo
    -------

    >>> seno(0)
    0.0
    '''

    return _math.sin(x)


@synonyms('cos')
def cosseno(x):
    '''Retorna o cosseno de x, onde x é medido em radianos.

    Pode ser chamada na forma curta (cos) ou longa (cosseno).

    Exemplo
    -------

    >>> cosseno(0)
    1.0
    '''

    return _math.cos(x)


@synonyms('tan', 'tg')
def tangente(x):
    '''Retorna a tangente de x, onde x é medido em radianos.

    Pode ser chamada na forma curta (tan) ou longa (tangente).

    Exemplo
    -------

    >>> tangente(0)
    0.0
    '''

    return _math.tan(x)


@synonyms('exp')
def exponencial(x):
    '''Retorna a exponencial de x.

    Pode ser chamada na forma curta (exp) ou longa (exponencial).

    Exemplo
    -------

    >>> exponencial(1)
    2.718281828459045
    '''

    return _math.exp(x)


@synonyms('log', 'ln')
def logarítimo(x):
    '''Retorna o logarítimo natural de x.

    Pode ser chamada na forma curta (log) ou longa (logarítimo).

    Exemplo
    -------

    >>> logarítimo(1)
    0.0
    '''

    return _math.log(x)


def log10(x):
    '''Retorna o logarítimo de x na base 10.

    Exemplo
    -------

    >>> log10(10)
    1.0
    '''
    return _math.log10(x)


#
# Controle de arredondamento e sinal dos números
#
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


def sinal(x):
    '''Retorna 1, -1 ou 0, dependendo do sinal de x.


    Exemplo
    -------

    >>> sinal(-32.0)
    -1
    '''
    if x == 0:
        return 0
    elif x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        raise ValueError('argumento não possui sinal definido')


@synonyms('arredonde')
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


@synonyms('trunque')
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


#
# Funções em listas de números
#
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


def todos(sequência):
    '''Retorna Verdadeiro se todos os objetos da sequência dada forem
    verdadeiros e Falso caso contrário.

    Exemplo
    -------

    >>> todos([Verdadeiro, Verdadeiro])  # doctest: +SKIP
    Verdadeiro
    >>> todos([Verdadeiro, Falso])       # doctest: +SKIP
    Falso
    '''

    return all(sequência)


def algum(sequência):
    '''Retorna Verdadeiro se algum dos objetos da sequência dada for
    verdadeiro e Falso caso contrário.

    Exemplo
    -------

    >>> algum([Verdadeiro, Verdadeiro])  # doctest: +SKIP
    Verdadeiro
    >>> algum([Verdadeiro, Falso])       # doctest: +SKIP
    Falso
    '''

    return any(sequência)


#
# Números aleatórios
#
def aleatório():
    '''Retorna um número aleatório no intervalo [0, 1]'''

    return _random.random()


def inteiro_aleatório(início, fim):
    '''Retorna um inteiro aleatório dentro do intervalo [início, fim]'''

    return _random.randint(início, fim)


@synonyms('lance_dados')
def lançar_dado():
    '''Retorna um número aleatório entre 1 e 6, como num lance de dados
    comuns'''

    return _random.randint(1, 6)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
