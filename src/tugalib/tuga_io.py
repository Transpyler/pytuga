'''
Funções de entrada e saída
==========================

Funções que realizam a interação com o usuário, seja lendo valores digitados
ou arquivos, seja mostrando valores na tela.
'''

from tugalib.util import synonyms


@synonyms('mostre')
def mostrar(objeto):
    '''Mostra o objeto ou texto fornecido na tela

    Exemplo
    -------

    >>> mostrar("Olá, mundo!")
    Olá, mundo!
    '''

    print(objeto)


@synonyms('leia_texto')
def ler_texto(mensagem):
    '''Pede ao usuário uma entrada de texto.

    Exemplo
    -------

    >>> nome = ler_texto('Seu nome: ')
    >>> mostrar("olá, " + nome)  # usuário digita "maria"
    olá, maria
    '''

    mensagem = mensagem + ' ' if not mensagem.endswith(' ') else mensagem
    return input(mensagem)


@synonyms('leia_número')
def ler_número(mensagem):
    '''Pede ao usuário uma entrada numérica.

    Exemplo
    -------

    >>> x = ler_número('Um número: ')  # usuário digita um 2...
    >>> x + 40
    42
    '''

    mensagem = mensagem + ' ' if not mensagem.endswith(' ') else mensagem
    num = float(input(mensagem).replace(',', '.'))
    return int(num) if int(num) == num else num


@synonyms('leia_arquivo')
def ler_arquivo(arquivo):
    '''Lê conteúdo de um arquivo texto e retorna uma string de texto.

    Exemplo
    -------

    >>> dados = ler_arquivo("foo.txt")
    '''

    return open(arquivo).read()


@synonyms('salve_arquivo')
def salvar_arquivo(arquivo, texto):
    '''Salva o conteúdo de texto no arquivo indicado, apagando qualquer
    conteúdo anterior.

    CUIDADO! Caso o arquivo dado exista, esta função sobrescreverá seu conteúdo
    sem perguntar nada!

    Exemplo
    -------

    >>> salvar_arquivo("foo.txt", dados)
    '''

    with open(arquivo) as F:
        F.write(str(texto))

if __name__ == '__main__':
    import doctest
    # doctest.testmod()
