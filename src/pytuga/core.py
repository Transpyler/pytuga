import builtins as _builtins
import importlib
from types import ModuleType as _Module

from pytuga import lib as tugalib
from pytuga.transpyler import pytuga_transpyler
from transpyler import utils as tuga_util

__all__ = [
    # Tugalib namespace
    'tugalib_namespace', 'init',

    # Compiling and executing
    'compile', 'transpile', 'exec', 'eval', 'is_incomplete_source',

    # Names and introspection
    'py_constants', 'constants',
    'py_exceptions', 'exceptions',
    'py_types', 'types',
    'py_functions', 'functions',
    'py_builtins', 'builtins',
]

# Save useful builtin functions
_compile = _builtins.compile
_exec = _builtins.exec
_eval = _builtins.eval
_input = _builtins.input
_print = _builtins.print
_locals = _builtins.locals

# Additional injected builtin names
_extra_builtins = set()


#
# Core API
#
def tugalib_namespace(forbidden=False):
    """
    Return a dictionary with all public tugalib functions.

    If forbidden is True, import the tugalib.tuga_forbidden module.
    """

    blacklist = {
        'tuga_draw', 'tuga_forbidden', 'tuga_io', 'tuga_math',
        'tuga_std', 'tuga_strings', 'turtlelib', 'util',
    }
    blacklist.update(dir(tuga_util))

    ns = {name: getattr(tugalib, name) for name in dir(tugalib)}

    if forbidden:
        mod = importlib.import_module('pytuga.lib.forbidden')
        for name in mod.__all__:
            ns[name] = getattr(mod, name)

    # Remove private methods, variables and forbidden values
    for name in list(ns):
        if name.startswith('_'):
            del ns[name]
        elif name.isupper():
            del ns[name]
        elif name in blacklist:
            del ns[name]

    return ns


def init(curses=True, extra_builtins=None):
    """
    Initializes pytuga runtime.

    Args:
        curses:
            Load forbidden part of pytuga.lib. This enables translation for
            builtin python types by hacking them at C-level.
        extra_builtins (dict):
            A dictionary with extra builtin functions to be added to the
            runtime.
    """

    pytuga_transpyler.init(curses=curses, extra_builtins=extra_builtins)


def compile(source, filename, mode, flags=0, dont_inherit=False,
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

    return pytuga_transpyler.compile(**_locals())


def exec(source, globals=None, locals=None, forbidden=False, builtins=False,
         exec_function=None):
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
            If given, update builtins with functions in tugalib.
        forbidden (bool):
            If true, initialize the forbidden lib functionality to enable i18n
            for Python builtins in C-level.
        exec_function (callable):
            A possible replacement for Python's built-in exec().
    """

    return pytuga_transpyler.exec(**_locals())


def eval(source, globals=None, locals=None, forbidden=False, builtins=False,
         eval_function=None):
    """
    Similar to the built-in function val() for Pytuguês code.

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
            If true, initialize the forbidden lib functionality to enable i18n
            for Python builtins in C-level.
        eval_function (callable):
            A possible replacement for Python's built-in eval().
    """

    return pytuga_transpyler.eval(**_locals())


def is_incomplete_source(src, filename="<input>", symbol="single"):
    """
    Test if a given pytuga code is incomplete.

    Incomplete code may appear in users interactions when user is typing a
    multi line command:

    para cada x de 1 ate 10:
        ... should continue here, but user already pressed enter!
    """

    return pytuga_transpyler.is_incomplete_source(**_locals())


def transpile(src):
    """
    Convert a Pytuguês/Pytuguese source to Python.
    """

    return pytuga_transpyler.transpile(src)


def tokenize(src):
    """
    Convert source to a list of tokens.
    """

    return list(pytuga_transpyler.lexer.tokenize(src))

#
# Pytuga introspections
#


def _filtering_out(names):
    """
    Remove name from global _names variable
    """

    for name in names:
        del _names[name]
    return names


all_names = [name for name in dir(tugalib) if not name.startswith('_')]
namespace = {name: getattr(tugalib, name) for name in all_names}
_names = namespace.copy()

# Classify names according to type: constants
_py_constants = (True, False, None)
py_constants = ['True', 'False', 'None']
constants = _filtering_out(
    [name for (name, value) in _names.items()
     if value in _py_constants or isinstance(value, (int, float))]
)

# Exceptions
py_exceptions = [
    name for (name, value) in vars(_builtins).items()
    if isinstance(value, type) and issubclass(value, Exception)
]
exceptions = _filtering_out(
    [name for (name, value) in _names.items()
     if isinstance(value, type) and issubclass(value, Exception)]
)

# Types
py_types = [
    name for (name, value) in vars(_builtins).items()
    if isinstance(value, type) and not issubclass(value, Exception)
]
types = _filtering_out(
    [name for (name, value) in _names.items() if isinstance(value, type)]
)

# Functions
py_functions = py_types = [
    name for (name, value) in vars(_builtins).items()
    if name not in py_types and name not in py_exceptions
]
functions = _filtering_out(
    [name for (name, value) in _names.items() if callable(value)]
)

# Modules
submodules = _filtering_out(
    [name for (name, value) in _names.items() if isinstance(value, _Module)]
)

# Builtins
py_builtins = py_types + py_functions
builtins = types + functions

# Builtins dictionary
_original_builtins = vars(_builtins)
