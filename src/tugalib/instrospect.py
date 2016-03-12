import tugalib
from types import ModuleType as _Module


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
    name for (name, value) in vars(__builtins__).items()
    if isinstance(value, type) and issubclass(value, Exception)
    ]
exceptions = _filtering_out(
        [name for (name, value) in _names.items()
         if isinstance(value, type) and issubclass(value, Exception)]
)

# Types
py_types = [
    name for (name, value) in vars(__builtins__).items()
    if isinstance(value, type) and not issubclass(value, Exception)
    ]
types = _filtering_out(
        [name for (name, value) in _names.items() if isinstance(value, type)]
)

# Functions
py_functions = py_types = [
    name for (name, value) in vars(__builtins__).items()
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
