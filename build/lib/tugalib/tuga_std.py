'''
Outras funções
==============

Outras funções que não se encaixam em nenhuma categoria específica.
'''
import time as _time
from tugalib.util import synonyms


#
# Controle de tempo e de saída do programa
#
@synonyms('durma')
def dormir(intervalo):
    '''Permanece sem fazer nada o intervalo de tempo fornecido (em segundos)'''

    _time.sleep(intervalo)


@synonyms('pausa', 'pause')
def pausar():
    '''Interrompe a execução até o usuário apertar a tecla <enter>'''

    input('')


@synonyms('termine')
def terminar():
    '''
    Termina a execução do programa.

    Semelhante à função sair(cod_erro), mas não requer a especificação de um
    código de erro'''

    sair(0)


@synonyms('saia')
def sair(código_erro):
    '''
    Termina a execução do programa fornecendo um código de erro ou código
    de saída.

    Um ``código_erro=0`` sinaliza que o programa terminou com sucesso. Qualquer
    outro número ou um texto representa falha'''

    raise SystemExit(código_erro)


#
# TODO: fazer funções com strings de documentação
#
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
verdadeiro = Verdadeiro = True
falso = Falso = False

if __name__ == '__main__':
    import doctest
    doctest.testmod()
