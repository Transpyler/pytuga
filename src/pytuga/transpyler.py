import sys

from transpyler import Transpyler
from transpyler.utils import pretty_callable
from . import __version__
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
    builtin_modules = ['pytuga.lib']

    def apply_curses(self):
        from pytuga.lib.curses import apply_curses
        apply_curses()

    def update_user_ns(self, ns):
        @pretty_callable(
            'digite "sair()" para terminar a execução',
            autoexec=True, autoexec_message='tchau! ;-)'
        )
        def sair():
            """
            Finaliza a execução do terminal de Pytuguês.
            """

            ns['exit']()

        ns['sair'] = sair


pytuga_transpyler = PytugaTranspyler()
PytugaTranspyler.banner = \
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


Bem-vindo ao Pytuguês, um Python com sotaque lusitano.

digite "ajuda()", "licença()" ou "tutorial()" para maiores informações.''' \
    % (__version__, sys.version.splitlines()[0])
