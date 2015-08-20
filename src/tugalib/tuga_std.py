'''
Outras funções
==============

Outras funções que não se encaixam em nenhuma categoria específica.
'''
import time as _time


def todos(sequência):
    '''Retorna Verdadeiro se todos os objetos da sequência dada forem
    verdadeiros e Falso caso contrário.

    Exemplo
    -------

    >>> todos([Verdadeiro, Verdadeiro])
    Verdadeiro
    >>> todos([Verdadeiro, Falso])
    Falso
    '''

    return all(sequência)


def algum(sequência):
    '''Retorna Verdadeiro se algum dos objetos da sequência dada for
    verdadeiro e Falso caso contrário.

    Exemplo
    -------

    >>> algum([Verdadeiro, Verdadeiro])
    Verdadeiro
    >>> algum([Verdadeiro, Falso])
    Falso
    '''

    return any(sequência)

#
# Controle do tempo
#


def dormir(intervalo):
    '''Permanece sem fazer nada o intervalo de tempo fornecido (em segundos)'''

    _time.sleep(intervalo)


def pausa():
    '''Interrompe a execução até o usuário apertar a tecla <enter>'''

    input('')


# TODO: fazer funções com strings de documentação

binário = bin
booleano = bool
# bytes = bytes
caractere = chr
dicionário = dict
enumerar = enumerate
real = float
formatar = format
ajuda = help
hexadecimal = hex
inteiro = int
tamanho = len
lista = list
octal = oct
#ord = ord
invertido = reversed
conjunto = set
ordenado = sorted
texto = str
tupla = tuple
tipo = type

if __name__ == '__main__':
    import doctest
    doctest.testmod()
