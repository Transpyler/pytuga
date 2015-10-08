'''
Funções de entrada e saída
==========================

Funções que realizam a interação com o usuário, seja lendo valores digitados
ou arquivos, seja mostrando valores na tela.
'''

from tugalib.util import synonyms


@synonyms('mostre')
def mostrar(objeto, *args):
    '''
    Mostra o objeto ou texto fornecido na tela.

    Se for chamada com vários argumentos, imprime os mesmos em sequência,
    separando com um espaço.

    Examples
    --------

    >>> mostrar("Olá, mundo!")
    Olá, mundo!
    '''

    print(objeto, *args)


@synonyms('leia_texto')
def ler_texto(mensagem):
    '''
    Pede ao usuário uma entrada de texto.

    Examples
    --------

    >>> nome = ler_texto('Seu nome: ')
    >>> mostrar("olá, " + nome)  # usuário digita "maria"
    olá, maria
    '''

    if isinstance(mensagem, str):
        mensagem = mensagem + ' ' if not mensagem.endswith(' ') else mensagem
    return input(mensagem)


@synonyms('leia_número')
def ler_número(mensagem):
    '''
    Pede ao usuário uma entrada numérica.

    Examples
    --------

    >>> x = ler_número('Um número: ')  # usuário digita um 2...
    >>> x + 40
    42
    '''

    texto = ler_texto(mensagem)
    num = float(texto.replace(',', '.'))
    return int(num) if int(num) == num else num


@synonyms('leia_arquivo')
def ler_arquivo(arquivo):
    '''
    Lê conteúdo de um arquivo texto e retorna uma string de texto.

    Examples
    --------

    >>> dados = ler_arquivo("foo.txt")
    '''

    return open(arquivo).read()


@synonyms('salve_arquivo')
def salvar_arquivo(arquivo, texto):
    '''
    Salva o conteúdo de texto no arquivo indicado, apagando qualquer
    conteúdo anterior.

    CUIDADO! Caso o arquivo dado exista, esta função sobrescreverá seu conteúdo
    sem perguntar nada!

    Examples
    --------

    >>> salvar_arquivo("foo.txt", dados)
    '''

    with open(arquivo) as F:
        F.write(str(texto))

if __name__ == '__main__':
    import doctest
    # doctest.testmod()
