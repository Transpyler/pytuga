import pytest
from pytuga.core import tugalib_namespace, update_builtins, revert_builtins
from pytuga.core import compile, transpile, exec


def test_namespace():
    ns = tugalib_namespace(forbidden=False)


def test_builtins():
    update_builtins(forbidden=False)
    assert raiz(4) == 2
    revert_builtins()

    with pytest.raises(NameError):
        assert raiz(4) == 2


def test_transpile():
    py = transpile('enquanto verdadeiro ou falso: prosseguir')
    # Each transpile call puts a '\n' in the end of line
    assert py == 'while True or False: pass\n'


def test_exec():
    D = {}
    exec('x = raiz(0 ou 1) ', D, forbidden=False)
    assert D['x'] == 1


def test_compile():
    code = compile('x = raiz(0 ou 1)', '<string>', 'exec')

    D = {}
    exec(code, D, forbidden=False)
    assert D['x'] == 1

    D = {}
    exec(code, D, forbidden=False)
    assert D['x'] == 1


if __name__ == '__main__':
    pytest.main('test_core.py')
