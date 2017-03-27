import contextlib
import builtins as _builtins
import importlib

from lazyutils import lazy


class Builtins:
    """
    Manage the builtin functions for the new language.
    """

    @lazy
    def modules(self):
        try:
            return list(self.language.builtin_modules)
        except (AttributeError, TypeError):
            return []

    @lazy
    def _namespace(self):
        ns = {}
        for mod in self.modules:
            mod = importlib.import_module(mod)
            for name in dir(mod):
                if name.startswith('_') or name.isupper():
                    continue
                ns[name] = getattr(mod, name)
        return ns

    def __init__(self, language=None):
        self.language = language

    def namespace(self):
        """
        Return a dictionary with all public functions.
        """

        return dict(self._namespace)

    def update(*args, **kwargs):
        """
        Update builtins with new functions.
        """

        self, *args = args
        ns = self._namespace
        ns.update(*args, **kwargs)

    @contextlib.contextmanager
    def restore_after(self):
        """
        Apply current builtins to Python's builtins module and restore
        state afterwards.
        """

        old_builtins = vars(_builtins)
        new_builtins = self.namespace()

        for k, v in new_builtins.items():
            setattr(_builtins, k, v)

        try:
            yield
        finally:
            for k in dir(_builtins):
                if k in new_builtins:
                    if k in old_builtins:
                        setattr(_builtins, k, old_builtins[k])
                    else:
                        delattr(_builtins, k)
