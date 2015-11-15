import os
import sys
import argparse
from pytuga.console import PyTugaConsole
from pytuga.lexer import transpile
from pytuga import __version__ as version


def start_interactive():
    '''Start Pytuga REPL'''

    from pytuga.console import run_console
    run_console()


def main():
    '''Executes the main pytuga program in the console.'''

    if len(sys.argv) <= 1:
        return start_interactive()

    # Process arguments
    parser = argparse.ArgumentParser(description='Executa código Pytuguês')
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
        help='mostra a versão do interpretador de pytuguês',
        action='version', version='Pytuga %s' % version)
    # parser.add_argument('--warning', '-w', action='store_const',
    #                   help='ativa avisos de compatibilidade com o python')
    args = parser.parse_args()

    # Process errors
    if os.path.splitext(args.arquivo)[1] != '.pytg':
        print('Aviso: Pytuga deve processar apenas arquivos .pytg!')
    if not os.path.exists(args.arquivo):
        raise SystemExit('O arquivo %s não existe!' % args.arquivo)

    # Process file
    if args.mostre_python:
        with open(args.arquivo) as F:
            print(transpile(F.read()))
    elif args.python:
        with open(args.arquivo) as source:
            with open(args.python, 'w') as dest:
                dest.write(transpile(source.read()))
    else:
        with open(args.arquivo) as F:
            console = PyTugaConsole(filename=args.arquivo)
            console.runcode(F.read())


if __name__ == '__main__':
    main()
