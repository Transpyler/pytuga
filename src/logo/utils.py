from functools import wraps as _wraps

from logo.mathutils import Vec as _Vec


def vecargsmethod(func):
    """
    Decorates a function of a vec object to accept the following signatures:

        func(vec, **kwds)
        func(x, y, **kwds)

    A Vec object is always passed to the given implementation.
    """
    @_wraps(func)
    def decorated(self, x, y=None, **kwds):
        if y is None:
            try:
                x, y = x
            except ValueError:
                raise ValueError('expected 2 elements, got %s' % len(x))

            return func(self, _Vec(x, y), **kwds)
        else:
            return func(self, _Vec(x, y), **kwds)
    return decorated


def alias(*args):
    """
    Set a list of function aliases for TurtleFunction methods.

    The aliases are automatically included in the resulting namespace.
    """

    def decorator(func):
        func.alias_list = args
        return func
    return decorator