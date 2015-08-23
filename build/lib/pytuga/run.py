'''
Script principal pytuga
'''
import sys
import argparse


def start_interactive():
    '''Inicia REPL'''


def run():
    '''Função principal de execução'''

    print(sys.argv)
    if len(sys.argv) <= 1:
        return start_interactive()

    parser = argparse.ArgumentParser(description='Executa código Pytuguês')
    parser.add_argument('arquivo', help='nome do arquivo a ser executado')
    # parser.add_argument('--warning', '-w', action='store_const',
    #                   help='ativa avisos de compatibilidade com o python')
    # parser.add_argument('--convert', '-c', action='store_const',
    #                   help='converte arquivo .pytg para .py')

    args = parser.parse_args()
    print(args)
