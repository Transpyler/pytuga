"""
Textos (strings)
================

Funções para processamento de texto.
"""

# TODO: terminar as traduções de funções e escolher ordem dos argumentos
from transpyler.utils import synonyms


#
# Unir e separar strings
#
@synonyms('concatene')
def concatenar(*args):
    """
    Converte os argumentos para texto e concatena o resultado

    Examples:
        >>> concatenar('x = ', 2)
        'x = 2'
    """

    return concatenar_lista(args)


@synonyms('concatene_lista')
def concatenar_lista(lista):
    """
    Converte os argumentos da lista em texto e concatena o resultado.

    Examples:
        >>> concatenar_lista(['a', 'b', 'c', 1, 2, 3])
        'abc123'
    """

    return ''.join(map(str, lista))


@synonyms('una_valores')
def unir_valores(separador, *args):
    """
    Semelhante à concatenar(), mas une os valores pelo texto separador
    especificado

    Examples:
        >>> unir_valores(', ', 1, 2, 3)
        '1, 2, 3'
    """

    return unir_lista(separador, args)


@synonyms('una_lista')
def unir_lista(separador, lista):
    """
    Semelhante à concatenar_lista(), mas une os valores pelo texto separador
    especificado

    Examples:
        >>> unir_lista(', ', [1, 2, 3])
        '1, 2, 3'
    """

    return str(separador).join(map(str, lista))


particionar = particione = str.partition
particionar_direita = particione_direita = str.rpartition
separar_texto = separe_texto = str.split
separar_em_linhas = separe_em_linhas = str.splitlines


# rsplit?


#
# Formatação
#
@synonyms('formate')
def formatar(texto, *args, **kwds):
    """
    Formata o texto inserindo os parâmetros dados nas posições coringa.

    Existem duas sintaxes diferentes para a formatação de texto. A primeira,
    baseada em C, utiliza o símbolo %s, %f, %d, etc para delimitar os pontos
    de inserção por posição.

    >>> formatar('%i = %.2f', 42, 42)
    '42 = 42.00'

    A segunda usa esta sintaxe (explicar!)

    >>> formatar('{0} = {1}', 42, 42)
    '42 = 42'
    """

    try:
        return texto % args
    except TypeError:
        return texto.format(*args, **kwds)


@synonyms('substitua')
def substituir(texto, valor, substituição):
    """
    Substitui no ``texto`` todas as ocorrências de ``valor`` pela
    ``substituição`` dada.

    Examples:
        >>> substituir('Olá, pessoal!', 'pessoal', 'mundo')
        'Olá, mundo!'
    """

    return str(texto).replace(valor, substituição)


# maketrans?
# translate?
# encode?
# format_map?


#
# Maiúsculas e minúsculas
#
def maiúsculas(texto):
    """
    Converte um texto para letras maiúsculas

    Examples:
        >>> maiúsculas('olá, mundo!')
        'OLÁ, MUNDO!'
    """

    return texto.upper()


def minúsculas(texto):
    """
    Converte um texto para letras minúsculas

    Examples:
        >>> minúsculas('OLÁ, MUNDO!')
        'olá, mundo!'
    """

    return texto.lower()


título = str.title
capitalizar = capitalize = str.capitalize
trocar_caso = troque_caso = str.swapcase
# casefold?


#
# Controle do espaço em branco
#
centralizar = centralize = str.center
justificar = justifique = justificar_esquerda = justifique_esquerda = str.ljust
justificar_direita = justifique_direita = str.rjust
remover_esquerda = remova_esquerda = str.lstrip
remover_direita = remova_direita = str.rstrip
remover = remova = str.strip
expandir_tabs = expanda_tabs = str.expandtabs
# zfill?

#
# Testes
#
começa_com = str.startswith
termina_com = str.endswith

é_minúsculo = str.islower
é_maiúsculo = str.isupper
é_título = str.istitle
é_alfanumérico = str.isalnum
é_alfabético = str.isalpha
é_identificador = str.isidentifier
é_decimal = str.isdecimal
é_digito = str.isdigit
é_numérico = str.isnumeric
é_imprimível = str.isprintable
é_espaço = str.isspace

#
# Procura
#
contar_em_texto = conte_em_texto = str.count
procurar_em_texto = procure_em_texto = str.find
procurar_em_texto_direita = procure_em_texto_direita = str.rfind
# index?, rindex?
