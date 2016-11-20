import importlib
import builtins as _builtins
from types import ModuleType as _Module
from pytuga import lib as tugalib
from pytuga import lexer
from pytuga import util as tuga_util


__all__ = [
    # Tugalib namespace
    'tugalib_namespace', 'update_builtins', 'revert_builtins',

    # Compiling and executing
    'compile', 'transpile', 'exec',

    # Names and introspection
    'py_constants', 'constants',
    'py_exceptions', 'exceptions',
    'py_types', 'types',
    'py_functions', 'functions',
    'py_builtins', 'builtins',
]


#
# Core API
#
def tugalib_namespace(forbidden=False):
    """Return all public tugalib functions.

    If forbidden is True, import the tugalib.tuga_forbidden module."""

    blacklist = {'tuga_draw', 'tuga_forbidden', 'tuga_io', 'tuga_math',
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


def update_builtins(forbidden=False):
    """Update Python's builtins with tugalib functions."""

    ns = tugalib_namespace(forbidden)
    for (name, value) in ns.items():
        setattr(_builtins, name, value)


def revert_builtins():
    """Remove pytuga functions from builtins"""

    tuganames = list(tugalib_namespace(forbidden=False))

    for name in tuganames:
        if hasattr(_builtins, name):
            delattr(_builtins, name)


def compile(source, filename, mode, flags=0, dont_inherit=False):
    """Similar to the built-in function compile().

    Works with Pytuguês code."""

    source = transpile(source)
    return __builtins__['compile'](source, filename, mode, flags, dont_inherit)


def exec(source, globals=None, locals=None, forbidden=False, builtins=False):
    """Similar to the built-in function exec().

    Works with Pytuguês code."""

    if globals is None:
        globals = {}

    if builtins:
        update_builtins(forbidden)
    else:
        globals.update(tugalib_namespace(forbidden))

    if isinstance(source, str):
        code = transpile(source)
    else:
        code = source

    return _builtins.exec(code, locals, globals)


def transpile(src):
    """Convert a Pytuguês (Pytuguese?) source to Python."""

    # Avoid problems with empty token streams
    if not src or src.isspace():
        return src

    # Convert and process...
    else:
        src_formatted = src

        if not src_formatted.endswith('\n'):
            src_formatted += '\n'

        tokens = lexer.fromstring(src_formatted)
        transpiled_tokens = lexer.transpile_tk(tokens)
        result = lexer.tostring(transpiled_tokens)
        return result


#
# Pytuga introspections
#
def _filtering_out(names):
    """Remove name from global _names variable"""
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
