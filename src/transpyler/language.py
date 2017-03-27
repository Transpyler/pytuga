import builtins as _builtins
import codeop

from lazyutils import lazy

from transpyler.builtins import Builtins
from transpyler.lexer import Lexer

# Save useful builtin functions
_compile = _builtins.compile
_exec = _builtins.exec
_eval = _builtins.eval
_input = _builtins.input
_print = _builtins.print


class Language:
    """
    Base class for a new transpyled language.

    Very simple Python variations can be created by subclassing Language::

        class PyBr(Language):
            translations = {
                'para': 'for',            # single token translations
                'em': 'in',
                ('para', 'cada'): 'for',  # token sequence translations
                ('faça', ':'): ':',
            }

    Now we can create an object with exec(), eval() and compile() functions that
    handle the newly defined language:

        pybr = PyBr()
        global_ns = {}

        pybr.exec('''
        x, y = 1, 1
        para cada i em [1, 2, 3, 4, 5] faça:
            x, y = y, x + y
        ''', global_ns)

        assert globals_ns['x'] == 8
        assert globals_ns['y'] == 13
    """
    name = None
    translations = None
    lexer_factory = Lexer
    builtins_factory = Builtins

    @lazy
    def lexer(self):
        return self.lexer_factory(self)

    @lazy
    def builtins(self):
        return self.builtins_factory(self)

    @lazy
    def _namespace_cache(self):
        return self.builtins_namespace()

    def __init__(self):
        self._forbidden = False

    def init(self, extra_builtins=None, forbidden=True):
        """
        Initializes language runtime.

        Args:
            forbidden:
                Load forbidden part of pytuga.lib. This enables translation for
                builtin python types by hacking them at C-level.
            extra_builtins (dict):
                A dictionary with extra builtin functions to be added to the
                runtime.
        """

        if forbidden:
            self.apply_forbidden()
        if extra_builtins:
            self.builtins.update(extra_builtins)

    def apply_forbidden(self):
        """

        Returns:

        """
        if self._forbidden is False:
            pass
        self._forbidden = True

    def compile(self, source, filename, mode, flags=0, dont_inherit=False,
                compile_function=None):
        """
        Similar to the built-in function compile() for Pytuguês code.

        The additional compile_function() argument allows to define a function to
        replace Python's builtin compile().

        Args:
            source (str or code):
                Code to be executed.
            filename:
                File name associated with code. Use '<input>' for strings.
            mode:
                One of 'exec' or 'eval'. The second allows only simple statements
                that generate a value and is used by the eval() function.
            forbidden (bool):
                If true, initialize the forbidden lib functionality to enable i18n
                for Python builtins in C-level.
            compile_function (callable):
                A possible replacement for Python's built-in compile().
        """

        source = self.transpile(source)
        compile_function = self.compile_function or self._compile
        return compile_function(source, filename, mode, flags, dont_inherit)

    def exec(self, source, globals=None, locals=None, forbidden=False,
             exec_function=None, builtins=False, _builtins_to_globals=True):
        """
        Similar to the built-in function exec() for Pytuguês code.

        The additional exec_function() argument allows to define a function to
        replace Python's builtin compile().

        Args:
            source (str or code):
                Code to be executed.
            globals, locals:
                A globals/locals dictionary
            builtins (bool):
                If given, execute with builtins injected on Python's builtins
                module.
            forbidden (bool):
                If true, initialize the forbidden lib functionality to enable i18n
                for Python builtins in C-level.
            exec_function (callable):
                A possible replacement for Python's built-in exec().
        """

        if builtins:
            with self.builtins.restore_after():
                return self.exec(source, globals, locals,
                                 forbidden=forbidden,
                                 _builtins_to_globals=False,
                                 exec_function=exec_function)

        exec_function = exec_function or _exec

        if globals is None:
            globals = _builtins.globals()
        if _builtins_to_globals:
            globals.update(self._namespace_cache)

        code = self.transpile(source) if isinstance(source, str) else source

        if locals is None:
            return exec_function(code, globals)
        else:
            return exec_function(code, globals, locals)

    def eval(self, source, globals=None, locals=None, forbidden=False,
             eval_function=None, builtins=False):
        """
        Similar to the built-in function eval() for transpyled code.

        The additional eval_function() argument allows to define a function to
        replace Python's builtin compile().

        Args:
            source (str or code):
                Code to be executed.
            globals, locals:
                A globals/locals dictionary
            builtins (bool):
                If given, update builtins with functions in tugalib.
            forbidden (bool):
                If true, initialize the forbidden lib functionality to enable
                i18n for Python builtins in C-level.
            eval_function (callable):
                A possible replacement for Python's built-in eval().
        """

        eval_function = eval_function or _eval
        return self.exec(source, globals, locals, forbidden=forbidden,
                         builtins=builtins, exec_function=eval_function)

    def transpile(self, src):
        """
        Convert source to Python.
        """

        return self.lexer.transpile(src)

    def is_incomplete_source(self, src, filename="<input>", symbol="single"):
        """
        Test if a given source code is incomplete.

        Incomplete code may appear in users interactions when user is typing a
        multi line command:

        for x in range(10):
            ... should continue here, but user already pressed enter!
        """

        pytuga_src = self.transpile(src)
        return codeop.compile_command(pytuga_src, filename, symbol) is None

    def builtins_namespace(self):
        """
        Return a dictionary with the default builtins namespace for language.
        """

        return self.builtins.namespace()
