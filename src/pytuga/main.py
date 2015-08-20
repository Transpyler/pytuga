'''
Script principal pytuga
'''
import os
import sys
import argparse


def start_interactive():
    '''Inicia REPL'''

    from pytuga.console import run_console
    run_console()


def run():
    '''Função principal de execução'''

    if len(sys.argv) <= 1:
        return start_interactive()

    # Processa argumentos
    parser = argparse.ArgumentParser(description='Executa código Pytuguês')
    parser.add_argument('arquivo', help='nome do arquivo a ser executado')
    # parser.add_argument('--warning', '-w', action='store_const',
    #                   help='ativa avisos de compatibilidade com o python')
    # parser.add_argument('--convert', '-c', action='store_const',
    #                   help='converte arquivo .pytg para .py')
    args = parser.parse_args()

    # Processa arquivo
    if os.path.splitext(args.arquivo)[1] != '.pytg':
        raise SystemExit('O Pytuga somente consegue processar arquivos .pytg!')
    elif not os.path.exists(args.arquivo):
        raise SystemExit('O arquivo %s não existe!' % args.arquivo)
    else:
        with open(args.arquivo) as F:
            from pytuga.console import PyTugaConsole
            console = PyTugaConsole(filename=args.arquivo)
            console.runcode(F.read())
