"""
Funções de entrada e saída
==========================

Funções que realizam a interação com o usuário, seja lendo valores digitados
ou arquivos, seja mostrando valores na tela.
"""

from transpyler.utils import synonyms


@synonyms('mostre')
def mostrar(*args):
    """
    Mostra o objeto ou texto fornecido na tela.

    Se for chamada com vários argumentos, imprime os mesmos em sequência,
    separando-os com um espaço.

    Examples:
        >>> mostrar("Olá, mundo!")
        Olá, mundo!
    """

    print(*args)


@synonyms('alerte', 'alertar')
def alerta(*args):
    """
    Similar à função `mostrar`, mas mostra a mensagem resultante em uma caixa
    de diálogo.
    """

    _alert(*args)


@synonyms('mostre_formatado', 'mostref', 'mostrarf')
def mostrar_formatado(texto, *args):
    """
    Mostra uma string de texto aplicando os argumentos de formatação
    fornecidos.
    """

    mostrar(texto % args)


@synonyms('leia_texto')
def ler_texto(mensagem=''):
    """
    Pede ao usuário uma entrada de texto.

    Examples:
        >>> nome = ler_texto('Seu nome: ')
        >>> mostrar("olá, " + nome)  # usuário digita "maria"
        olá, maria
    """

    if isinstance(mensagem, str) and mensagem:
        mensagem = (mensagem + ' ') if not mensagem.endswith(' ') else mensagem
    return _input(mensagem)


@synonyms('pausa', 'pause')
def pausar():
    """
    Interrompe a execução até o usuário apertar a tecla <enter>.
    """

    _pause()


@synonyms('leia_número')
def ler_número(mensagem=''):
    """
    Pede ao usuário uma entrada numérica.

    Examples:
        >>> x = ler_número('Um número: ')  # usuário digita um 2...
        >>> x + 40
        42
    """

    texto = ler_texto(mensagem)
    num = float(texto.replace(',', '.'))
    return int(num) if int(num) == num else num


@synonyms('leia_arquivo', 'leia_ficheiro', 'ler_ficheiro')
def ler_arquivo(arquivo=None):
    """
    Lê conteúdo de um arquivo texto e retorna uma string de texto.

    Examples:
        >>> dados = ler_arquivo("foo.txt")
    """

    if arquivo is None:
        arquivo = _filechooser(True)
    return open(arquivo).read()


@synonyms('salve_em_arquivo', 'salvar_em_ficheiro', 'salve_em_ficheiro')
def salvar_em_arquivo(texto, arquivo=None):
    """
    Salva o conteúdo de texto no arquivo indicado, apagando qualquer
    conteúdo anterior.

    CUIDADO! Caso o arquivo dado exista, esta função sobrescreverá seu conteúdo
    sem perguntar nada!

    Examples:
        >>> salvar_em_arquivo(dados, "foo.txt")
    """

    if arquivo is None:
        arquivo = _filechooser(False)

    with open(arquivo) as F:
        F.write(str(texto))


# These functions can be replaced/mocked by the Qt GUI and have a proper
# behavior in a graphical environment or in tests.
def _pause():
    ler_texto('Aperte <enter> para continuar')


def _alert(*args):
    mostrar(*args)


def _input(*args):
    return input(*args)


def _filechooser(do_open):
    return ler_texto('Nome do arquivo: ')
