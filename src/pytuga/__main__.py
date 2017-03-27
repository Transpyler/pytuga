import os
import sys
import argparse
import pytuga
from pytuga import transpile
from pytuga import __version__ as version


def start_simple_console():
    """
    Start console-based Pytuga REPL
    """

    from pytuga.console import run_console
    run_console()


def start_ipytuga(**kwargs):
    """
    Starts IPython-based Pytuga REPL.
    """

    from pytuga.ipytuga.shell import start_shell
    start_shell(**kwargs)


def start_qtconsole(**kwargs):
    """
    Starts a QtConsole based shell application.
    """

    from pytuga_gui.ipytuga_qtconsole import start_qtconsole
    start_qtconsole(**kwargs)


def start_full_gui(**kwargs):
    """
    Starts full GUI application.
    """

    from pytuga_gui.main_window import main


def to_python(src):
    """
    Convert script from pytugues to python.
    """

    return 'from pytuga.lib import *\n' + transpile(src)


def main(argv=None):
    """
    Executes the main pytuga program in the console.
    """

    if len(sys.argv) <= 1:
        return start_ipytuga()

    # Process arguments
    parser = argparse.ArgumentParser(description='Interpretador de Pytuguês')
    parser.add_argument(
        'arquivo', help='nome do arquivo a ser executado')
    parser.add_argument(
        '--mostre-python', '-P',
        help='mostra conversão do arquivo para Python na tela',
        action='store_const', const=True)
    parser.add_argument(
        '--python', '-p',
        metavar='ARQUIVO',
        help='salva conversão para Python no caminho especificado')
    parser.add_argument(
        '--versão', '-v',
        help='mostra a versão do interpretador de Pytuguês',
        action='version', version='Pytuga %s' % version)
    parser.add_argument(
        '--console', '-c',
        action='store_const', const=True,
        help='inicia console simples, sem editor de texto.'
    )
    parser.add_argument(
        '--terminal', '-t',
        action='store_const', const=True,
        help='inicia shell Pytuguês em modo não-gráfico.'
    )
    # parser.add_argument('--warning', '-w', action='store_const',
    #                   help='ativa avisos de compatibilidade com o python')
    args = parser.parse_args(argv)

    # Process errors
    if not os.path.exists(args.arquivo):
        raise SystemExit('O arquivo %s não existe!' % args.arquivo)
    if os.path.splitext(args.arquivo)[1] != '.pytg':
        print('Aviso: Pytuga deve processar apenas arquivos .pytg!')

    # Process file
    if args.mostre_python:
        with open(args.arquivo) as F:
            print(to_python(F.read()))
    elif args.python:
        with open(args.arquivo) as source:
            data = to_python(source.read())
        with open(args.python, 'w') as dest:
            dest.write(data)
    else:
        with open(args.arquivo) as F:
            data = F.read()
        pytuga.init()
        code = pytuga.compile(data, args.arquivo, 'exec')
        pytuga.exec(code, {})


if __name__ == '__main__':
    main(['-h'])
