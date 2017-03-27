from lazyutils import lazy


class Instrospection:
    """
    Introspections facilities for a transpyled Language.
    """

    # Original python names
    py_constants = ['True', 'False', 'None']

    @lazy
    def py_exceptions(self):
        return [
            name for (name, value) in vars(_builtins).items()
            if isinstance(value, type) and issubclass(value, Exception)
            ]

    @lazy
    def py_types(self):
        return [
            name for (name, value) in vars(_builtins).items()
            if isinstance(value, type) and not issubclass(value, Exception)
            ]

    @lazy
    def py_functions(self):
        return [
            name for (name, value) in vars(_builtins).items()
            if name not in self.py_types and name not in self.py_exceptions
            ]

    @lazy
    def py_builtins(self):
        return self.py_types + self.py_functions

    def __init__(self, language):
        self.language = language


        # def _filtering_out(self, names):
        #     """
        #     Remove name from global _names variable
        #     """
        #
        #     for name in names:
        #         del _names[name]
        #     return names
        #
        # all_names = [name for name in dir(tugalib) if not name.startswith('_')]
        # namespace = {name: getattr(tugalib, name) for name in all_names}
        # _names = namespace.copy()
        #
        # # Classify names according to type: constants
        # constants = _filtering_out(
        #     [name for (name, value) in _names.items()
        #      if value in _py_constants or isinstance(value, (int, float))]
        # )
        #
        # # Exceptions
        # exceptions = _filtering_out(
        #     [name for (name, value) in _names.items()
        #      if isinstance(value, type) and issubclass(value, Exception)]
        # )
        #
        # # Types
        # types = _filtering_out(
        #     [name for (name, value) in _names.items() if isinstance(value, type)]
        # )
        #
        # # Functions
        # functions = _filtering_out(
        #     [name for (name, value) in _names.items() if callable(value)]
        # )
        #
        # # Modules
        # submodules = _filtering_out(
        #     [name for (name, value) in _names.items() if isinstance(value, _Module)]
        # )
        #
        # # Builtins
        # builtins = types + functions
        #
        # # Builtins dictionary
        # _original_builtins = vars(_builtins)