import pytest

from transpyler import Language


@pytest.fixture
def python():
    """
    A new language that makes no changes in comparison with the default
    interpreter.
    """

    class Python(Language):
        pass

    return Python()


@pytest.fixture
def pybr():
    """
    A new language that makes no changes in comparison with the default
    interpreter.
    """

    class PyBr(Language):
        translations = {
            'para': 'for',
            'em': 'in',
            ('para', 'cada'): 'for',
            ('faça', ':'): ':',
        }
        builtin_modules = ['math']

    return PyBr()


@pytest.fixture
def pybr_code():
    return '''
x, y = 1, 1
para cada i em [1, 2, 3, 4, 5] faça:
    x, y = y, x + y
'''
