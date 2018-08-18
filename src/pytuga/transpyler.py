import sys

from transpyler import Transpyler
from transpyler.curses import curse_none_repr, curse_bool_repr, apply_curses
from transpyler.utils import pretty_callable
from . import __version__
from . import curses
from .keywords import TRANSLATIONS, SEQUENCE_TRANSLATIONS, ERROR_GROUPS
from .lexer import PytugaLexer


class PytugaTranspyler(Transpyler):
    """
    Pytuguês support.
    """

    name = 'pytuga'
    display_name = 'Pytuguês'
    lexer_factory = PytugaLexer
    translations = dict(TRANSLATIONS)
    translations.update(SEQUENCE_TRANSLATIONS)
    error_dict = ERROR_GROUPS
    lang = 'pt_BR'

    def apply_curses(self):
        """
        Apply all curses.
        """

        curse_none_repr('Nulo')
        curse_bool_repr('Verdadeiro', 'Falso')
        apply_curses({
            list: curses.Lista,
            tuple: curses.Tupla,
            set: curses.Conjunto,
            dict: curses.Dicionário,
            str: curses.Texto,
        })

    def __make_global_namespace(self):
        ns = super().make_global_namespace()
        exit_function = ns['exit']

        @pretty_callable(
            'digite "sair()" para terminar a execução',
            autoexec=True, autoexec_message='tchau! ;-)'
        )
        def sair():
            """
            Finaliza a execução do terminal de Pytuguês.
            """

            exit_function()

        # Update exit function and Python constants.
        ns.update(
            sair=sair,
            Verdadeiro=True,
            verdadeiro=True,
            Falso=False,
            false=False,
            Nulo=None,
            nulo=None,
        )
        return ns


# TODO: Add the help string once we implement those functions.
# # HELP = (
# #     '\n\n'
# #     'digite "ajuda()", "licença()" ou "tutorial()" para maiores informações.'
# )
HELP = ''

PytugaTranspyler.short_banner = \
    '''Pytuga %s
Python %s

Bem-vindo ao Pytuguês, um Python com sotaque lusitano.''' \
    % (__version__, sys.version.splitlines()[0]) + HELP

PytugaTranspyler.long_banner = \
    r'''Pytuga %s
Python %s
                 __
                /\ \__
 _____    __  __\ \ ,_\  __  __     __       __
/\ '__`\ /\ \/\ \\ \ \/ /\ \/\ \  /'_ `\   /'__`\
\ \ \L\ \\ \ \_\ \\ \ \_\ \ \_\ \/\ \L\ \ /\ \L\.\_
 \ \ ,__/ \/`____ \\ \__\\ \____/\ \____ \\ \__/.\_\
  \ \ \/   `/___/> \\/__/ \/___/  \/___L\ \\/__/\/_/
   \ \_\      /\___/                /\____/
    \/_/      \/__/                 \/___/


Bem-vindo ao Pytuguês, um Python com sotaque lusitano.''' \
    % (__version__, sys.version.splitlines()[0]) + HELP
