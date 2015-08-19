'''
Funções de entrada e saída
==========================

Funções que realizam a interação com o usuário, seja lendo valores digitados
ou arquivos, seja mostrando valores na tela.
'''


def mostre(objeto):
    '''Mostra o objeto ou texto fornecido na tela

    Exemplo
    -------

    >>> mostre("Olá, mundo!")
    Olá, mundo!
    '''

    print(objeto)
mostrar = mostre


def leia_texto(mensagem):
    '''Pede ao usuário uma entrada de texto.

    Exemplo
    -------

    >>> nome = leia_texto('Seu nome: ')
    >>> mostre("olá, " + nome)  # usuário digita "maria"
    olá, maria
    '''

    mensagem = mensagem + ' ' if not mensagem.endswith(' ') else mensagem
    return input(mensagem)
ler_texto = leia_texto


def leia_número(mensagem):
    '''Pede ao usuário uma entrada numérica.

    Exemplo
    -------

    >>> x = leia_número('Um número: ')  # usuário digita um 2...
    >>> x + 40
    42
    '''

    mensagem = mensagem + ' ' if not mensagem.endswith(' ') else mensagem
    num = float(input(mensagem).replace(',', '.'))
    return int(num) if int(num) == num else num
ler_número = leia_número


def leia_arquivo(arquivo):
    '''Lê conteúdo de um arquivo texto e retorna uma string de texto.

    Exemplo
    -------

    >>> dados = leia_arquivo("foo.txt")
    '''

    return open(arquivo).read()
ler_arquivo = leia_arquivo


def salve_arquivo(arquivo, texto):
    '''Salva o conteúdo de texto no arquivo indicado.

    Exemplo
    -------

    >>> salve_arquivo("foo.txt", dados)
    '''

    with open(arquivo) as F:
        F.write(texto)
salvar_arquivo = salve_arquivo
