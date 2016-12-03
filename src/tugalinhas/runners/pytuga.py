from .python import PythonRunner


class PyTugaRunner(PythonRunner):
    """
    Executes code in Pytuga environment.
    """

    def __init__(self, namespace=None, **kwds):
        import pytuga
        import pytuga.lib.tuga_io
        self._pytuga = pytuga
        self._exec = pytuga.exec

        super().__init__(namespace={}, **kwds)

        # Update some functions in the tuga_io module to use the desired
        # qt-aware implementation. This is kind of ugly, but we will go with it
        # for now ;-)
        pytuga.lib.tuga_io._input = self._namespace['input']
        pytuga.lib.tuga_io._alert = self._namespace.pop('alert')
        pytuga.lib.tuga_io._pause = self._namespace.pop('pause')
        pytuga.lib.tuga_io._filechooser = self._namespace.pop('filechooser')

        # Configure the default namespace and initialize runner
        _namespace = pytuga.tugalib_namespace(forbidden=True)
        _namespace.update(dict(namespace or {}))
        self._namespace.update(_namespace)

    def transform(self, src):
        return self._pytuga.transpile(src)
